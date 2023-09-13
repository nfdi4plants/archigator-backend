import os
import requests
import json
from bs4 import BeautifulSoup

from .models.record import *
from app.invenio.models.draft_response import Draft
from app.invenio.models.community_review_respone import CommunityReview
from app.gitlab.models.user import User
from app.invenio.models.request import *
from app.invenio.models.review import *
from app.invenio.models.draft_file import DraftFile


class Invenio_API:
    def __init__(self):
        self.api_token = os.environ.get("INVENIO_API_TOKEN")
        self.api_url = os.environ.get("INVENIO_API_URL")
        self.username = os.environ.get("INVENIO_USERNAME")
        self.headers = {"Authorization": f'{"Bearer "}{self.api_token}'}
        self.api_path = "/api"
        self.community_id = os.environ.get("INVENIO_COMMUNITY_ID")

        print("credentials:\n")
        print(self.api_token)

    # def create_draft(self, data):
    #     path = "/records/"
    #     api_url = f'{self.api_url}{self.api_path}{path}'

    def submit_draft_record(self, record: Record, record_id):
        path = f'{"/records/"}{record_id}{"/draft/actions/submit-review"}'
        api_url = f'{self.api_url}{self.api_path}{path}'

        resp = requests.post(
            api_url,
            headers=self.headers,
            timeout=20,
            verify=False,
            json=record.json()
        )

    def create_draft(self, record_model):
        path = "/records"

        api_url = f'{self.api_url}{self.api_path}{path}'

        data = json.dumps(json.loads(record_model.json()))

        print("draft put model", record_model.dict())

        try:

            response = requests.post(
                api_url,
                headers=self.headers,
                timeout=20,
                verify=False,
                data=json.dumps(json.loads(record_model.json()))
            )

            response.raise_for_status()
            response_json = response.json()

            print("response put model create", response_json)

            draft_response = Draft(**response_json)
            return draft_response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def update_draft(self, record_id, record_model):
        path = "/records/"

        api_url = f'{self.api_url}{self.api_path}{path}{record_id}{"/draft"}'

        data = json.dumps(json.loads(record_model.json()))

        print("draft put model", record_model.dict())

        try:

            response = requests.put(
                api_url,
                headers=self.headers,
                timeout=20,
                verify=False,
                data=json.dumps(json.loads(record_model.json()))
            )

            response.raise_for_status()
            response_json = response.json()

            print("response put model update", response_json)

            draft_response = Draft(**response_json)
            return draft_response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def create_draft_review(self, record_id):
        path = f'{"/records/"}{record_id}{"/draft/review"}'
        api_url = f'{self.api_url}{self.api_path}{path}'

        header = {'Content-type': 'application/json'}

        newdict = {}
        newdict.update(self.headers)
        newdict.update(header)

        print("newd", newdict)

        data = {
            "receiver": {
                "community": self.community_id
                # "community": "a6dfa9ba-788e-4611-a5f4-289d28cdda53"
            },
            "type": "community-submission"
        }

        try:

            response = requests.put(
                api_url,
                headers=newdict,
                timeout=20,
                verify=False,
                data=json.dumps(data)
            )

            response.raise_for_status()
            response_json = response.json()

            review_response = CommunityReview(**response_json)
            return review_response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def submit_draft_review(self, record_id: str, user_model: User):
        path = f'{"/records/"}{record_id}{"/draft/actions/submit-review"}'
        api_url = f'{self.api_url}{self.api_path}{path}'

        print("user", user_model.name)
        print("user", user_model.email)

        header = {'Content-Type': 'application/json'}
        modified_headers = {}
        modified_headers.update(self.headers)
        modified_headers.update(header)

        print(header)

        # user_string = "Name: " + str(
        #     user_model.name) + "\n" + "Email: " + user_model.email + "\n" + "Created at: " + user_model.created_at + "\n" + "URL: " + user_model.web_url + "\n"
        #
        # data = {
        #     "payload": {
        #         "content": "The following user has submitted an review. \n" + user_string,
        #         "format": "html"
        #     }
        # }

        data = {
            "payload": {
                "content": "Project has been submitted, please wait for review.",
                "format": "html"
            }
        }


        print("data", data)

        try:

            response = requests.post(
                api_url,
                headers=modified_headers,
                timeout=20,
                verify=False,
                json=data
            )

            print("responsee", response)
            print(response.content)

            # response.raise_for_status()

            return response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def start_draft_file_upload(self, record_id: int, filelist: list):
        path = "/records/"
        draft_path = "/draft/files"

        api_url = f'{self.api_url}{self.api_path}{path}{record_id}{draft_path}'

        files = []

        for file in filelist:
            files.append({"key": file})

        print("filelist", files)

        try:

            response = requests.post(
                api_url,
                headers=self.headers,
                timeout=20,
                verify=False,
                data=json.dumps(files)
            )

            response.raise_for_status()
            response_json = response.json()

            # draft_response = Draft(**response_json)
            return response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def upload_draft_content(self, record_id: int, filename: str, file):
        path = "/records/"
        draft_path = "/draft/files/"

        api_url = f'{self.api_url}{self.api_path}{path}{record_id}{draft_path}{filename}{"/content"}'

        header = {'Content-type': 'application/octet-stream'}

        updated_header = {}
        updated_header.update(self.headers)
        updated_header.update(header)

        try:

            response = requests.put(
                api_url,
                headers=updated_header,
                timeout=20,
                verify=False,
                data=file
            )

            print(response)
            print(response.content)
            response.raise_for_status()
            response_json = response.json()

            return response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def complete_draft_upload(self, record_id: int, filename: str):
        path = "/records/"
        draft_path = "/draft/files/"

        api_url = f'{self.api_url}{self.api_path}{path}{record_id}{draft_path}{filename}{"/commit"}'

        try:

            response = requests.post(
                api_url,
                headers=self.headers,
                timeout=20,
                verify=False,
                # data=json.dumps(files)
                # data=upload_file
            )

            print(response)
            print(response.content)
            response.raise_for_status()
            response_json = response.json()

            return response

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_request(self, request_id: str):
        path = "/requests/"

        api_url = f'{self.api_url}{self.api_path}{path}{request_id}'

        try:

            # response = requests.get(
            #     api_url,
            #     headers=self.headers,
            #     timeout=20,
            #     verify=False,
            #     # data=json.dumps(files)
            #     # data=upload_file
            # )

            response = requests.get(api_url, timeout=5, headers=self.headers, verify=False)

            print("failed to get request", response)
            print(response.content)
            response.raise_for_status()
            response_json = response.json()

            print("failed to get request" ,response_json)

            request = Request(**response_json)

            print("ereqst", request)

            return request

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def get_review(self, record_id: str):
        path = "/records/"
        review_path = "/draft/review"


        api_url = f'{self.api_url}{self.api_path}{path}{record_id}{review_path}'

        try:
            response = requests.get(api_url, timeout=5, headers=self.headers, verify=False)

            print("response", response)
            print(response.content)
            response.raise_for_status()
            response_json = response.json()
            print("res", response_json)

            review = Review(**response_json)

            return review

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


    def get_comments(self, request_id: str):
        path = "/requests/"
        timeline_path = "/timeline"


        api_url = f'{self.api_url}{self.api_path}{path}{request_id}{timeline_path}'

        try:
            response = requests.get(api_url, timeout=5, headers=self.headers, verify=False)

            comments = []

            print("response", response)
            print(response.content)
            response.raise_for_status()
            response_json = response.json()
            print("res", response_json)

            # data = json.loads(json_data)

            # contents = [hit["payload"]["content"] for hit in response_json["hits"]["hits"] if "content" in hit["payload"]]
            contents = [BeautifulSoup(hit["payload"]["content"], "html.parser").text for hit in
                        response_json["hits"]["hits"] if "content" in hit["payload"]]

            for content in contents:
                print(content)
                comments.append(content)

            print("comments", comments)

            # review = Review(**response_json)

            return comments

        except requests.exceptions.HTTPError as errh:
            raise Exception(errh) from errh
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


















