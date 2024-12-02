from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.middlewares.http_basic_auth import *
from app.api.models.setup.project import TestMail
from app.tasks.email.send_mail import send_curator_mail

router = APIRouter()

@router.post("/send_test_curator_mail", summary="Send test mail", status_code=status.HTTP_201_CREATED,
             response_class=Response, dependencies=[Depends(basic_auth)],
             description="Send Curator Test Mail")
async def send_test_mail(request: Request, payload: TestMail, background_tasks: BackgroundTasks):

    username = payload.username
    project_name = payload.projectname
    submission_url = payload.submission_url

    curator_mail = os.environ.get("CURATOR_MAIL", None)
    curator_mail = curator_mail.split(',')


    background_tasks.add_task(send_curator_mail, curator_mail, username, project_name, submission_url)
    return Response(status_code=status.HTTP_201_CREATED)