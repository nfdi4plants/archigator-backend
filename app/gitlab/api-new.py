import requests
import os
import pydantic
import json
import logging

from dotenv import load_dotenv

from .models.project import *
from .models.pipeline import *
from .models.user import *
from .models.test_report import *
from .models.report_summary import *
from .models.badges import *
from app.invenio.models.record import Metadata
from app.gitlab.models.setup_system_hook import *

import sys


class Gitlab_API:
    def __init__(self):
        self.api_token = os.environ.get("GITLAB_API_TOKEN")
        self.api_url = os.environ.get("GITLAB_API_URL")
        self.headers = {"Authorization": f'{"Bearer "}{self.api_token}'}
        self.api_path = "/api/v4"

    def _make_request(self, url, method="GET", data=None, params=None):
        try:
            response = requests.request(method, url, timeout=5, headers=self.headers, params=params, json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_project(self, project_id) -> Union[Project, None]:
        path = "/projects/"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}'
        response = self._make_request(api_url)

        if response is not None:
            print(response.status_code)
            project = Project(**response.json())
            return project

        return None

    def get_userid_by_mail(self, email) -> Union[User, None]:
        path = "/users"
        api_url = f'{self.api_url}{self.api_path}{path}'
        params = {"search": email}

        response = self._make_request(api_url, params=params)

        if response is not None:
            print(response.status_code)
            user = User(**response.json()[0])
            return user

        return None

    def userid_is_member(self, userid, project_id) -> bool:
        path = "/projects/"
        member_path = "/members"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{member_path}'

        response = self._make_request(api_url)
        members = response.json()
        is_member = any(member["id"] == userid for member in members)

        if is_member:
            return True

        return False

    def get_memberids(self, project_id) -> list:
        path = "/projects/"
        members_path = "/members"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{members_path}'

        user_ids = []
        response = self._make_request(api_url)

        if response:
            user_ids = [member.get("id") for member in response.json()]
            return user_ids

        return []

    def get_user(self, user_id) -> Union[User, None]:
        path = "/users/"
        api_url = f'{self.api_url}{self.api_path}{path}{user_id}'

        response = self._make_request(api_url)

        if response is not None:
            user = User(**response.json())
            return user

        return None

    def get_latest_pipeline(self, project_id) -> Union[Pipeline, None]:
        path = "/projects/"
        pipeline_path = "/pipelines/latest"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{pipeline_path}'

        response = self._make_request(api_url)

        if response is not None:
            pipeline = Pipeline(**response.json())
            return pipeline

        return None

    def get_test_report(self, project_id, pipeline_id) -> Union[TestReport, None]:
        path = "/projects/"
        pipeline_path = "/pipelines/"
        report_path = "/test_report"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{pipeline_path}{pipeline_id}{report_path}'
        response = self._make_request(api_url)

        if response is not None:
            report = TestReport(**response.json())
            return report

        return None

    def get_test_summary(self, project_id, pipeline_id) -> Union[TestSummary, None]:
        path = "/projects/"
        pipeline_path = "/pipelines/"
        report_path = "/test_report_summary"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{pipeline_path}{pipeline_id}{report_path}'

        response = self._make_request(api_url)

        if response is not None:
            report = TestReport(**response.json())
            return report

        return None

    def list_badges(self, project_id) -> Union[BadgeList, None]:
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}'
        response = self._make_request(api_url)

        if response is not None:
            badge_list = BadgeList(__root__=response.json())
            return badge_list

        return None

    def get_badge(self, project_id, badge_id) -> Union[Badge, None]:
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}{badge_id}'
        response = self._make_request(api_url)

        if response is not None:
            badge = Badge(**response.json())
            return badge

        return None

    def edit_badge(self, project_id, badge_id, badge_data) -> bool:
        path = f"/projects/{project_id}/badges/{badge_id}"
        api_url = f'{self.api_url}{self.api_path}{path}'

        response_data, status_code = self._make_request(api_url, method="PUT", data=badge_data.dict())

        # if status_code == 200:
        #     return True
        return status_code == 200

    def add_badge(self, project_id: int, badge_data: BadgeEdit) -> Union[BadgeEdit, None]:
        path = "/projects/"
        badge_path = "/badges"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}'
        response = self._make_request(api_url, method="POST", data=badge_data.dict())

        if response is not None:
            badge = Badge(**response.json())
            return badge

        return None

    def remove_badge(self, project_id: int, badge_id: int) -> bool:
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}{badge_id}'

        response, status_code = self._make_request(api_url, method="DELETE")

        if status_code == 200:
            return True
        else:
            return False


    def get_job_artifact(self, project_id: int, branch: str, filename: str, job_name: str):
        path = "/projects/"
        job_path = "/jobs/artifacts/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{job_path}{branch}/raw/{filename}?job={job_name}'

        response = self._make_request(api_url)

        if response is not None:
            return response.content

        return None

    def list_projects(self) -> list:
        path = "/projects/"
        api_url = f'{self.api_url}{self.api_path}{path}'

        response = self._make_request(api_url)

        if response is not None:
            project_list = ProjectList(projects=response.json())
            return project_list.projects

        return []

    def add_systemhook(self, hook: AddSystemHook) -> bool:
        path = "/hooks/"
        api_url = f'{self.api_url}{self.api_path}{path}'
        response, status_code = self._make_request(api_url, method="POST", data=hook.dict())

        if status_code == 200:
            return True
        else:
            return False


