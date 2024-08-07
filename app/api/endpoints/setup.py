from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.helpers.link_generator import LinkGenerator
from app.tasks.setup.add_badge import setup_project
from app.tasks.setup.setup_all_projects import setup_projects, delete_badges
from app.api.models.setup.project import Project, Projects
from app.api.middlewares.http_basic_auth import *
from app.tasks.setup.install_systemhook import *

router = APIRouter()


@router.post("/project", summary="Setup", status_code=status.HTTP_201_CREATED,
             response_class=Response, dependencies=[Depends(basic_auth)], description="Install badges for one project.")
async def install_project(request: Request, payload: Project, background_tasks: BackgroundTasks):
    background_tasks.add_task(setup_project, payload.project_id, payload.overwrite)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/projects", summary="Setup", status_code=status.HTTP_201_CREATED,
             response_class=Response, dependencies=[Depends(basic_auth)],
             description="Installs badges for all projects.")
async def install_projects(request: Request, payload: Projects, background_tasks: BackgroundTasks):
    background_tasks.add_task(setup_projects, payload.overwrite)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/delete_badges", summary="Setup", status_code=status.HTTP_201_CREATED,
             response_class=Response, dependencies=[Depends(basic_auth)],
             description="Removes badges in all projects.")
async def install_projects(request: Request, payload: Projects, background_tasks: BackgroundTasks):
    background_tasks.add_task(delete_badges)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/hook", summary="Setup", status_code=status.HTTP_201_CREATED,
             response_class=JSONResponse, dependencies=[Depends(basic_auth)],
             description="Installs the required systemhook")
async def install_hook(request: Request):
    token = install_systemhook()
    print("tt", token)

    hook_response = SystemhookSetupResponse(token=token)

    response_json = jsonable_encoder(hook_response)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=response_json)


@router.post("/generatelink", summary="Setup", status_code=status.HTTP_200_OK,
             response_class=Response, dependencies=[Depends(basic_auth)],
             description="Generates a Link for a badge button. Usage directly in Gitlab Filehook.")
async def generate_link(request: Request, payload: Project):

    # classe generate_link aufrufen
    filehook_link_generator = LinkGenerator()
    filehook_link = filehook_link_generator.generate_link(payload.project_id)

    # return json mit link

    response = {
        "link": filehook_link
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=response)