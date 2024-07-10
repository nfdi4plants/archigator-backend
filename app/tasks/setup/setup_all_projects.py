from app.gitlab.api import Gitlab_API
from app.gitlab.models.badges import *
from app.helpers.hmac_generator import HmacGenerator

from app.gitlab.models.project import Project, ProjectList
from app.tasks.setup.add_badge import setup_project, delete_project_badge


def setup_projects(overwrite:bool = False):

    preinstall_badges = ["pipeline-badge", "publish-badge"]

    print("in setup project")
    gitlab_api = Gitlab_API()

    projects_list = gitlab_api.list_projects()
    print("project_list", projects_list)


    projectid_list = []

    for projects in projects_list:
        projectid_list.append(projects.id)

    print("project_idlist", projectid_list)


    for project in projects_list:
        print(project.id)
        setup_project(project_id=project.id, overwrite=overwrite)



def delete_badges():

    print("in deleting badges")
    gitlab_api = Gitlab_API()

    projects_list = gitlab_api.list_projects()


    projectid_list = []

    for projects in projects_list:
        projectid_list.append(projects.id)

    print("project_idlist", projectid_list)


    for project in projects_list:
        print(project.id)
        delete_project_badge(project_id=project.id)



