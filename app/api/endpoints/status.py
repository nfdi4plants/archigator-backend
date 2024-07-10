import jwt
import os

from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import Union

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
from app.api.models.status_response import StatusResponse, Gituser, ProjectPipeline, UserProject, Test
from app.gitlab.models.test_report import *

from app.api.models.error_response import *
from app.invenio.models.record import Metadata

# from app.api.middlewares.jwt_authentication import jwt_authentication
from app.api.middlewares.jwt_authentication import JWTBearer
from app.api.models.jw_token import JwtToken

router = APIRouter()


@router.get("", summary="Gitlab", status_code=status.HTTP_200_OK,
            response_model=StatusResponse,
            responses={200: {"model": StatusResponse}, 500: {"model": StatusResponse}},
            dependencies=[Depends(JWTBearer())])
# async def status(request: Request, payload: Status):
async def status(authorization: str = Header(..., description="Bearer token", include_in_schema=False)):
    # body = await request.body()

    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        jwt_token = JwtToken(**decoded_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    gitlab_api = Gitlab_API()

    if jwt_token.project_id is None:
        return HTTPException(status_code=404)

    print("proejct")
    # project = gitlab_api.get_project(payload.project_id)

    try:
        project = gitlab_api.get_project(jwt_token.project_id)
    except:
        project = None

    # print("project", project)
    #
    # print(project.owner)
    # print(project.id)

    project_pipeline = None

    print("pipeleine")
    try:
        pipeline = gitlab_api.get_latest_pipeline(project.id)
        print("pipeline id", pipeline.id)
        project_pipeline = ProjectPipeline(status=pipeline.status, finished_at=pipeline.finished_at,
                                           web_url=pipeline.web_url, tests=[])

        print("prp", project_pipeline)
    except:
        pipeline = None

    try:
        if pipeline is not None:
            test_report = gitlab_api.get_test_report(project.id, pipeline.id)

            print("tt", test_report)
            print(test_report.test_suites)
            print("test cases etc....\n")
            tests = []
            for suite in test_report.test_suites:
                print(suite.name)
                print(suite.test_cases)
                for test_case in suite.test_cases:
                    print(test_case.status)
                    print(test_case.name.strip("[]"))
                    test = Test(name=test_case.name.strip("[]"), status=test_case.status)
                    tests.append(test)
            project_pipeline.tests = tests
        else:
            test_report = []
    except:
        test_report = None

    try:
        user = gitlab_api.get_user(project.owner.id)
        print("user", user)
    except:
        user = None

    try:
        metadata = gitlab_api.get_job_artifact(project_id=project.id, branch="main", filename="metadata.json",
                                               job_name="generate_metadata")
        print(metadata.title)
    except:
        print("no metadata available")
        metadata = None

    # response = StatusResponse(pipeline_status=pipeline.status, project_name=project.name,
    #                           user=Gituser(name=user.name, email=user.email, avatar_url=user.avatar_url,
    #                                        ip_address=user.last_sign_in_ip, username=user.username,
    #                                        web_url=user.web_url),
    #                           metadata=metadata,
    #                           pipeline=ProjectPipeline(status=pipeline.status, finished_at=pipeline.finished_at,
    #                                                    web_url=pipeline.web_url,tests=tests),
    #                           project=UserProject(name=project.name, web_url=project.web_url))

    response = StatusResponse(user=user,
                              metadata=metadata,
                              pipeline=project_pipeline,
                              project=project)

    response_json = jsonable_encoder(response)

    return JSONResponse(response_json)
