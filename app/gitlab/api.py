import requests
import os
import pydantic
import json
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
        load_dotenv()
        self.api_token = os.environ.get("GITLAB_API_TOKEN")
        self.api_url = os.environ.get("GITLAB_API_URL")
        self.headers = {"Authorization": f'{"Bearer "}{self.api_token}'}
        self.api_path = "/api/v4"


    def _make_request(self, url, method="GET", data=None):
        try:
            response = requests.request(method, url, timeout=5, headers=self.headers, json=data)
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

    def get_project(self, project_id):
        path = "/projects/"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}'

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            print(response.status_code)
            response.raise_for_status()
            response_json = response.json()
            project = Project(**response_json)
            return project
        except requests.exceptions.HTTPError as errh:
            print(errh)
            print("no project found")
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_userid_by_mail(self, email):
        path = "/users"
        # api_url = f'{self.api_url}{self.api_path}{path}' +'?search=marcel.tschoepe@rz.uni-freiburg.de'
        api_url = f'{self.api_url}{self.api_path}{path}'
        params = {"search": email}

        try:
            # response = requests.get(api_url, timeout=5, headers=self.headers, params=params)
            response = requests.get(api_url, headers=self.headers, params=params)
            response.raise_for_status()
            response_json = response.json()[0]
            user = User(**response_json)
            return user
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
            # print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_project_members(self,project_id):
        url = f"{self.api_url}/projects/{project_id}/members"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            members = response.json()
            return [member['id'] for member in members]
        return []

    def get_groups_with_access_to_project(self, project_id):
        url = f"{self.api_url}/projects/{project_id}/shared_groups"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            groups = response.json()
            return [group['group_id'] for group in groups]
        return []

    def get_group_members(self, group_id):
        url = f"{self.api_url}/groups/{group_id}/members"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            members = response.json()
            return [member['id'] for member in members]
        return []

    def get_project_and_group_members(project_id):
        project_members = self.get_project_members(project_id)
        groups_with_access = self.get_groups_with_access_to_project(project_id)
        group_members = []
        for group_id in groups_with_access:
            group_members.extend(self.get_group_members(group_id))
        return project_members, group_members


    def userid_is_member(self, userid, project_id):
        self.get_project_and_group_members(project_id)
        project_members, group_members = get_project_and_group_members(project_id)

        members = project_members + group_members

        is_member = any(member["id"] == userid for member in members)

        if is_member:
            return True
        else:
            return False



    def userid_is_member_old(self, userid, project_id):
        path = "/projects/"
        member_path = "/members"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{member_path}'

        try:
            # response = requests.get(api_url, timeout=5, headers=self.headers, params=params)
            response = requests.get(api_url, headers=self.headers, timeout=5)
            response.raise_for_status()
            members = response.json()
            is_member = any(member["id"] == userid for member in members)

            if is_member:
                return True
            return False
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
            # print(errh)
            return False
        except requests.exceptions.ConnectionError as errc:
            print(errc)
            return False
        except requests.exceptions.Timeout as errt:
            print(errt)
            return False
        except requests.exceptions.RequestException as err:
            print(err)
            return False

    def get_memberids(self, project_id):
        path = "/projects/"
        members_path = "/members"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{members_path}'

        # print(api_url)
        try:
            user_ids = []
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            print("resp", response_json)

            for member in response_json:
                user_id = member.get("id", None)
                user_ids.append(user_id)

            return user_ids
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
            # print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_user(self, user_id):
        path = "/users/"
        api_url = f'{self.api_url}{self.api_path}{path}{user_id}'

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            print("resp", response_json)
            user = User(**response_json)
            return user
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
            # print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_latest_pipeline(self, project_id):
        path = "/projects/"
        pipeline_path = "/pipelines/latest"
        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{pipeline_path}'

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            pipeline = Pipeline(**response_json)
            return pipeline
        except requests.exceptions.HTTPError as errh:
            print("no pipeline found")
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_test_report(self, project_id, pipeline_id):
        path = "/projects/"
        pipeline_path = "/pipelines/"
        report_path = "/test_report"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{pipeline_path}{pipeline_id}{report_path}'

        print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()
            # response_json = response.content
            print("response json", type(response_json))
            print("response json", response_json)
            # print("resp json", json.loads(response_json))
            report = TestReport(**response_json)
            return report
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_test_summary(self, project_id, pipeline_id):
        path = "/projects/"
        pipeline_path = "/pipelines/"
        report_path = "/test_report_summary"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{pipeline_path}{pipeline_id}{report_path}'

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()

            # print("-->", response_json)

            report_summary = TestSummary(**response_json)
            return report_summary
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def list_badges(self, project_id):
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}'

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()

            print("list -->", response_json)
            resp = {"list": response_json}

            print("to badgelist")
            badge_list = BadgeList(__root__=response_json)
            print("after badgelist")
            return badge_list
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_badge(self, project_id, badge_id):
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}{badge_id}'

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            badge = Badge(**response_json)
            return badge
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def edit_badge(self, project_id, badge_id, badge_data: BadgeEdit):
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}{badge_id}'
        print("putting badge")
        print("badge_data", badge_data)
        # print("badge_data", json.dumps(badge_data))

        badge_data = badge_data.dict()
        print("--", badge_data)

        # print(api_url)
        try:
            response = requests.put(api_url, timeout=5, headers=self.headers, data=badge_data)
            print("after put")
            print(response.content)
            print(api_url)
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            # badge = Badge(**response_json)
            # return badge
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def add_badge(self, project_id: int, badge_data: BadgeEdit):
        path = "/projects/"
        badge_path = "/badges"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}'
        print("adding badge")
        print("badge_data", badge_data)
        # print("badge_data", json.dumps(badge_data))

        badge_data = badge_data.dict()
        print("--", badge_data)

        # print(api_url)
        try:
            response = requests.post(api_url, timeout=5, headers=self.headers, data=badge_data)
            print(response.content)
            print(api_url)
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            badge = Badge(**response_json)
            return badge
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    def remove_badge(self, project_id: int, badge_id: int):
        path = "/projects/"
        badge_path = "/badges/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{badge_path}{badge_id}'
        # print("badge_data", json.dumps(badge_data))

        # print(api_url)
        try:
            response = requests.delete(api_url, timeout=5, headers=self.headers)
            print(response.content)
            print(api_url)
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            # badge = Badge(**response_json)
            # return badge
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_job_artifact(self, project_id: int, branch: str, filename: str, job_name: str):
        path = "/projects/"
        job_path = "/jobs/artifacts/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{job_path}{branch}/raw/{filename}?job={job_name}'
        # + "?job=create metadata"

        # print(api_url)

        response = requests.get(api_url, timeout=5, headers=self.headers)
        print(response.content)
        print(api_url)
        print("..--")
        response.raise_for_status()
        response_json = response.json()

        print("-->", response_json)

        # metadata = Metadata(**response_json)
        # print("metadata filled")
        print("now returning")
        return response.json()

        # try:
        #     response = requests.get(api_url, timeout=5, headers=self.headers)
        #     print(response.content)
        #     print(api_url)
        #     print("..--")
        #     response.raise_for_status()
        #     response_json = response.json()
        #
        #     print("-->", response_json)
        #
        #     metadata = Metadata(**response_json)
        #     return metadata
        # except requests.exceptions.HTTPError as errh:
        #     raise Exception(errh) from errh
        # except requests.exceptions.ConnectionError as errc:
        #     print(errc)
        # except requests.exceptions.Timeout as errt:
        #     print(errt)
        # except requests.exceptions.RequestException as err:
        #     print(err)

    def get_job_artifact_arcjson(self, project_id: int, branch: str, filename: str, job_name: str):
        path = "/projects/"
        job_path = "/jobs/artifacts/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{job_path}{branch}/raw/{filename}?job={job_name}'
        # + "?job=create metadata"

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            print(response.content)
            print(api_url)
            print("..")
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            # metadata = Metadata(**response_json)

            return response_json
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    def get_job_artifact_md(self, project_id: int, branch: str, filename: str, job_name: str):
        path = "/projects/"
        job_path = "/jobs/artifacts/"

        api_url = f'{self.api_url}{self.api_path}{path}{project_id}{job_path}{branch}/raw/{filename}?job={job_name}'
        # + "?job=create metadata"

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            print(response.content)
            print(api_url)
            print("..")
            response.raise_for_status()
            # response_json = response.json()#


            # print("-->", response_json)

            # metadata = Metadata(**response_json)

            return response.content
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def list_projects(self):
        path = "/projects/"

        api_url = f'{self.api_url}{self.api_path}{path}'
        print(api_url)
        # + "?job=create metadata"

        # print(api_url)
        try:
            response = requests.get(api_url, timeout=5, headers=self.headers)
            print(response.content)
            print(api_url)
            print("..")
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            project_list = ProjectList(projects=response_json)
            return project_list.projects
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def add_systemhook(self, hook: AddSystemHook):
        path = "/hooks/"

        api_url = f'{self.api_url}{self.api_path}{path}'
        # print("badge_data", json.dumps(badge_data))

        hook_data = hook.dict()
        print("--", hook)

        # print(api_url)
        try:
            response = requests.post(api_url, timeout=5, headers=self.headers, data=hook_data)
            print(response.content)
            print(api_url)
            response.raise_for_status()
            response_json = response.json()

            print("-->", response_json)

            return response.status_code
        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
