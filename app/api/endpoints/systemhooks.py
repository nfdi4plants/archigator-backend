from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, BackgroundTasks
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
from app.tasks.setup.add_badge import setup_project

router = APIRouter()


@router.post("/systemhook", summary="Gitlab Systemhook", status_code=status.HTTP_204_NO_CONTENT,
             response_class=Response)
async def ontology(request: Request, payload: Union[GitlabWebhook, SystemHookCreate, SystemHook_Push],
                   background_tasks: BackgroundTasks):
    # body = await request.body()

    print("payload", payload.dict())

    print(payload.event_name)

    print("project id is: ", payload.project_id)

    gitlab_api = Gitlab_API()
    # project = gitlab_api.get_project(payload.project_id)

    if payload.event_name == "push":
        print("push event triggered")

    if payload.event_name == "project_create":
        print("project was created")

        # setup_project(payload.project_id)
        background_tasks.add_task(setup_project(payload.project_id))

    # if webhook is a release then:
    # get userid from project_id
    # get pipeline status
    # if pipeline was successful:
    # get zip from pipeline
    # create draft
    # create draft_review
    # upload to invenio

    # return Response(status_code=status.HTTP_204_NO_CONTENT)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
