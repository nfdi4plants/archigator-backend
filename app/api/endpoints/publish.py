import os
import sys
from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, Header, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import Union, Annotated

from app.api.models.access_token import AccessToken
# from ..models.gitlab_webhook import GitlabWebhook
# from ..models.test_response import TestResponse
from app.api.models.test_response import TestResponse
from app.api.models.gitlab_webhook import GitlabWebhook
from app.gitlab.models.system_hook_create import SystemHookCreate
from app.gitlab.models.system_hook_push import SystemHook_Push

from app.gitlab.api import Gitlab_API
from app.gitlab.models.badges import *

from app.helpers.hmac_generator import HmacGenerator
from app.api.models.status import Status
from app.api.models.jw_token import JwtToken
from app.api.models.status_response import StatusResponse, Gituser, ProjectPipeline, UserProject, Test
from app.gitlab.models.test_report import *

from app.invenio.api import *

from app.invenio.models.record import *

from app.api.models.error_response import *
from app.invenio.models.record import Metadata, Record
from app.api.middlewares.jwt_authentication import JWTBearer
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.api.models.publish.publish_response import Publication
from app.tasks.email.send_mail import send_testmail, send_mail, send_curator_mail

from app.api.middlewares.oauth_authentication import *

import jwt

router = APIRouter()

security_scheme = HTTPBearer()


# security = HTTPAuthorizationCredentials()


def remove_email_identifiers(metadata: Metadata) -> Metadata:
    if metadata.creators:
        for creator in metadata.creators:
            if creator.person_or_org.identifiers:
                # Use list comprehension to filter out identifiers with scheme="email"
                creator.person_or_org.identifiers = [
                    identifier
                    for identifier in creator.person_or_org.identifiers
                    if identifier.scheme != "email"
                ]

    return metadata


@router.post("", summary="Publish", status_code=status.HTTP_201_CREATED, response_class=Response,
             dependencies=[Depends(validate_access_token)], responses={200: {"model": Publication}})
async def publish_project(request: Request, background_tasks: BackgroundTasks,
                          publication: str = Header(..., description="Bearer token", include_in_schema=True),
                          access_token: AccessToken = Depends(validate_access_token)):
    access_token = AccessToken(**access_token)
    try:
        scheme, token = publication.split(" ")
        if scheme.lower() != "token":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.environ.get("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        jwt_token = JwtToken(**decoded_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    gitlab_api = Gitlab_API()

    try:
        project = gitlab_api.get_project(jwt_token.project_id)
    except:
        raise HTTPException(status_code=403, detail="Could not retrieve project details.")

    # try:
    #     user = gitlab_api.get_user(project.owner.id)
    # except:
    #     raise HTTPException(status_code=403, detail="User information could not be retrieved.")

    try:
        # user = gitlab_api.get_user(project.owner.id)
        user = gitlab_api.get_userid_by_mail(access_token.preferred_username)
    except:
        raise HTTPException(status_code=403, detail="User information could not be retrieved.")

    try:
        is_member = gitlab_api.userid_is_member(user.id, project.id)
    except:
        raise HTTPException(status_code=403, detail="Could not retrieve membership")

    if not is_member:
        raise HTTPException(status_code=403, detail="You must be member of this project to publish.")

    try:
        pipeline = gitlab_api.get_latest_pipeline(project.id)
    except:
        raise HTTPException(status_code=403, detail="Pipeline details could not be retrieved.")

    if pipeline.status != "success":
        print("pipeline not succeded, cancel request")
        raise HTTPException(status_code=403, detail="The project must pass all tests before it can be published.")

    try:
        metadata = gitlab_api.get_job_artifact(project_id=project.id, branch="main", filename="metadata.json",
                                               job_name="create metadata")
    except:
        raise HTTPException(status_code=403, detail="No metadata available.")

    print("metadata", metadata)

    metadata_model = Metadata(**metadata)

    identifier_url = f"https://git.nfdi4plants.org/projects/{project.id}"

    identifier_list = []

    identifier_list.append(Identifier(scheme="url", identifier=identifier_url))

    metadata_model.identifiers = identifier_list

    metadata_model.description = f"hosted on: https://git.nfdi4plants.org/projects/{project.id}"

    metadata_model = remove_email_identifiers(metadata_model)

    print("metadata", metadata)

    invenio_api = Invenio_API()

    data_object = []

    record = Record(access=Access(record="public", files="public"), files=Files(enabled=True,
                                                                                default_preview="arc-summary.md",
                                                                                order=["arc-summary.md", "arc.json"]),
                    metadata=metadata_model)

    try:
        draft_record = invenio_api.create_draft(record)
        record_id = draft_record.id
    except:
        raise HTTPException(status_code=403, detail="Unable to create an Invenio draft record.")

    # record_id = draft_record.id

    try:
        archive_file = gitlab_api.get_job_artifact_arcjson(project_id=project.id, branch="main", filename="arc.json",
                                                           job_name="create ARC JSON")
        summary_file = gitlab_api.get_job_artifact_md(project_id=project.id, branch="main",
                                                      filename="arc-summary.md", job_name="create ARC JSON")

    except:
        raise HTTPException(status_code=403, detail="Couldn't retrieve arc.json")

    try:
        invenio_api.start_draft_file_upload(record_id, ["arc.json", "arc-summary.md"])
        invenio_api.upload_draft_content(record_id, "arc.json", json.dumps(archive_file))
        invenio_api.complete_draft_upload(record_id=record_id, filename="arc.json")

        # invenio_api.start_draft_file_upload(record_id, ["arc-summary.md"])
        invenio_api.upload_draft_content(record_id, "arc-summary.md", summary_file)
        invenio_api.complete_draft_upload(record_id=record_id, filename="arc-summary.md")

        invenio_api.update_draft(record_id=record_id, record_model=record)

    except:
        raise HTTPException(status_code=403, detail="Could not upload arc.json as draft upload.")

    try:
        blu = invenio_api.create_draft_review(record_id)
        print(blu)
    except:
        raise HTTPException(status_code=403, detail="Couldn't create draft review.")

    # add archive to draft

    print("user", user)
    # sys.exit()

    try:
        draft = invenio_api.submit_draft_review(record_id=record_id, user_model=user)
    except:
        print("could not submit draft")
        raise HTTPException(status_code=403, detail="Couldn't submit draft review.")

    # try:
    #     metadata = gitlab_api.get_job_artifact(project_id=project.id, branch="main", filename="metadata.json",
    #                                            job_name="create metadata")
    #     print(metadata.title)
    # except:
    #     print("not metadata")
    #     metadata = None

    print("\n\ngetting record review etc....\n\n")
    review = invenio_api.get_review(record_id)

    user_mails = []
    user_mails.append(user.email)

    try:
        member_ids = gitlab_api.get_memberids(project_id=project.id)
        for user_id in member_ids:
            member_user = gitlab_api.get_user(user_id)
            user_mails.append(member_user.email)
    except:
        user_mails = []
        user_mails.append(user.email)

    try:
        # review = invenio_api.get_review(record_id)
        # print("review", review)
        # print("\n\n")
        # print("review id", review.id)
        # request_id = review.id
        request_id = review.id

        archigator_url = os.getenv("ARCHIGATOR_URL", "http://localhost:8000")

        hmac_generator = HmacGenerator(os.getenv("ARCHIGATOR_SECRET"))
        signature = hmac_generator.generate_order_signature(project.id, request_id)

        print("signature", signature)

        order_url = hmac_generator.build_url(archigator_url, "order",
                                             publication=signature)
    except:
        order_url = None

    print("user", user.name)
    print("project", project.name)
    print("id", review.id)
    print("order", order_url)

    publication = Publication(user=user.name, project_name=project.name, record_id=record_id, order_url=order_url,
                              token=signature)

    # return Response(status_code=201)
    # return "bla"
    response_json = jsonable_encoder(publication)

    mail_enabled = os.getenv("EMAIL_ENABLED", False)

    print("\n\n\n email is enabled?", mail_enabled)

    print("user email is", user.email)

    submission_url = "https://archive.nfdi4plants.org/communities/dataplant/requests/"
    submission_url = submission_url + review.id
    curator_mail = os.environ.get("CURATOR_MAIL", None)
    curator_mail = list(set(curator_mail))

    user_mails = list(set(user_mails))

    if mail_enabled:
        background_tasks.add_task(send_mail, user_mails, user.name, project.name, order_url)

        if curator_mail:
            background_tasks.add_task(send_curator_mail, curator_mail, user.name, project.name, submission_url)
    return JSONResponse(status_code=201, content=response_json)
