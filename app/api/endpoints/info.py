import jwt
import os

from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import Union

from app.api.models.access_token import AccessToken
from app.gitlab.api import Gitlab_API
from app.api.models.status_response import StatusResponse, Gituser, ProjectPipeline, UserProject, Test, Tests, Receipt
from app.invenio.api import Invenio_API
from app.invenio.models.record import Metadata
from app.api.models.jw_token import JwtToken, OrderToken

from app.api.middlewares.oauth_authentication import *

router = APIRouter()

@router.get("/owner", summary="Project owner information", status_code=status.HTTP_200_OK,
            response_model=Gituser,
            responses={200: {"model": Gituser}, 500: {"model": Gituser}},
            dependencies=[Depends(validate_access_token)])
async def owner(publication: str = Header(..., description="Bearer token"),
                access_token: AccessToken = Depends(validate_access_token)):
    access_token = AccessToken(**access_token)
    try:
        print("publication", publication)
        scheme, token = publication.split(" ")
        print("token", token)
        if scheme.lower() != "token":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        jwt_token = JwtToken(**decoded_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    gitlab_api = Gitlab_API()

    if jwt_token.project_id is None:
        return HTTPException(status_code=404)

    try:
        project = gitlab_api.get_project(jwt_token.project_id)
    except:
        project = None


    try:
        print("email is", access_token.preferred_username)
        user = gitlab_api.get_userid_by_mail(access_token.preferred_username)
        print("userid", user.id)
    except:
        print("no user found")
        user = None

    # try:
    #     is_member = gitlab_api.userid_is_member(user.id, project.id)
    # except:
    #     is_member = False

    # try:
    #     user = gitlab_api.get_user(project.owner.id)
    #     print("user", user)
    # except:
    #     user = None

    is_member = gitlab_api.userid_is_member(user.id, project.id)
    print("is_member", is_member)


    try:
        response = Gituser(name=user.name, username=user.username, avatar_url=user.avatar_url,
                           web_url=user.web_url, email=user.email, is_member=is_member, project_url=project.web_url)
    except:
        response = Gituser()

    response_json = jsonable_encoder(response)

    return JSONResponse(response_json)


@router.get("/project", summary="Project information", status_code=status.HTTP_200_OK,
            response_model=UserProject,
            responses={200: {"model": UserProject}, 500: {"model": UserProject}},
            dependencies=[Depends(validate_access_token)])
async def project(publication: str = Header(..., description="Bearer token")):
    try:
        scheme, token = publication.split(" ")
        if scheme.lower() != "token":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        jwt_token = JwtToken(**decoded_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    gitlab_api = Gitlab_API()

    if jwt_token.project_id is None:
        return HTTPException(status_code=404)

    try:
        project = gitlab_api.get_project(jwt_token.project_id)
    except:
        project = None

    try:
        pipeline = gitlab_api.get_latest_pipeline(project.id)
        project_pipeline = ProjectPipeline(status=pipeline.status, finished_at=pipeline.finished_at,
                                           web_url=pipeline.web_url, tests=[])
    except:
        pipeline = None

    try:
        response = UserProject(name=project.name, web_url=project.web_url, status=pipeline.status,
                               avatar_url=project.avatar_url)
    except:
        response = Gituser()

    response_json = jsonable_encoder(response)

    return JSONResponse(response_json)


@router.get("/tests", summary="Project Pipeline Tests", status_code=status.HTTP_200_OK,
            response_model=Tests,
            responses={200: {"model": Tests}, 500: {"model": Tests}},
            dependencies=[Depends(validate_access_token)])
async def tests(publication: str = Header(..., description="Bearer token", include_in_schema=True)):
    try:
        scheme, token = publication.split(" ")
        if scheme.lower() != "token":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        jwt_token = JwtToken(**decoded_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    gitlab_api = Gitlab_API()

    if jwt_token.project_id is None:
        return HTTPException(status_code=404)

    try:
        project = gitlab_api.get_project(jwt_token.project_id)
    except:
        project = None

    try:
        pipeline = gitlab_api.get_latest_pipeline(project.id)
        project_pipeline = ProjectPipeline(status=pipeline.status, finished_at=pipeline.finished_at,
                                           web_url=pipeline.web_url, tests=[])
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
                    if test_case.status == "success":
                        continue
                    print(test_case.status)
                    print(test_case.name.strip("[]"))
                    print("case", test_case)

                    system_output = ""
                    if test_case.system_output is not None:
                        system_output =  test_case.system_output.get("message", "")
                    test = Test(name=test_case.name.strip("[]"), status=test_case.status,
                                system_output=system_output)
                    tests.append(test)
            project_pipeline.tests = tests
        else:
            test_report = []
    except:
        test_report = []

    try:
        print("report", test_report)
        response = Tests(__root__=project_pipeline.tests)
    except:
        response = Tests(__root__=[])

    response_json = jsonable_encoder(response)

    return JSONResponse(response_json)


@router.get("/metadata", summary="Metadata information", status_code=status.HTTP_200_OK,
            response_model=UserProject,
            responses={200: {"model": UserProject}, 500: {"model": UserProject}},
            dependencies=[Depends(validate_access_token)])
async def metadata(publication: str = Header(..., description="Bearer token", include_in_schema=True)):
    try:
        scheme, token = publication.split(" ")
        if scheme.lower() != "token":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        jwt_token = JwtToken(**decoded_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    gitlab_api = Gitlab_API()

    if jwt_token.project_id is None:
        return HTTPException(status_code=404)

    try:
        project = gitlab_api.get_project(jwt_token.project_id)
    except:
        project = None

    try:
        metadata = gitlab_api.get_job_artifact(project_id=project.id, branch="main", filename="metadata.json",
                                               job_name="generate_metadata")
        print("got metadata from", metadata)
        # print(metadata.title)
    except:
        print("no metadata available")
        metadata = None

    response = Metadata(**metadata)

    try:
        print("metadata", metadata)
        # print(metadata.creators)
        # response = Metadata(creators=metadata.creators, publication_date=metadata.publication_date,
        #                     resource_type=metadata.resource_type, title=metadata.title)
        response = Metadata(**metadata)
    except:
        response = Metadata()

    response_json = jsonable_encoder(response)

    return JSONResponse(response_json)


# @router.get("/status/{project_id}/{request_id}", summary="Receipt information", status_code=status.HTTP_200_OK,
#             response_model=UserProject,
#             responses={200: {"model": Receipt}, 500: {"model": Receipt}},
#             dependencies=[Depends(JWTBearer())])
@router.get("/order", summary="Receipt information", status_code=status.HTTP_200_OK,
            responses={200: {"model": Receipt}, 500: {"model": Receipt}})
            # dependencies=[Depends(JWTBearer())])
async def receipt(publication: str = Header(..., description="Bearer token")):
    try:
        print("publication", publication)
        scheme, token = publication.split(" ")
        print("scheme", scheme)
        print("token", token)
        if scheme.lower() != "token":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        print("dec token", decoded_token)
        jwt_token = OrderToken(**decoded_token)
        print("jwtr ", jwt_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    print("getting receipt")
    gitlab_api = Gitlab_API()
    invenio_api = Invenio_API()

    # if jwt_token.project_id is None:
    #     return HTTPException(status_code=404)

    try:
        # project = gitlab_api.get_project(jwt_token.project_id)
        project = gitlab_api.get_project(jwt_token.project_id)
        print("project", project)
    except:
        project = None

    try:
        print("trying getting request")
        review = invenio_api.get_request(jwt_token.request_id)
        # review = invenio_api.get_request("71d0aa32-472b-4fb1-bcf3-6a85bdbcc162")

    except:
        review = Request()

    try:
        comments = invenio_api.get_comments(jwt_token.request_id)
    except:
        comments = []

    print(project.name)
    print(project.web_url)
    print(project.owner.name)
    print(review.status)

    try:
        receipt = Receipt(status=review.status, web_url=project.web_url, project_owner=project.owner.name,
                          project_name=project.name, comments=comments, order_id=review.id)
    except:
        receipt = Receipt()

    # response_json = jsonable_encoder(response)
    response_json = jsonable_encoder(receipt)

    return JSONResponse(response_json)
