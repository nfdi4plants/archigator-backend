import os

from app.api.models.setup.project import Project
from app.gitlab.api import Gitlab_API
from app.helpers.hmac_generator import HmacGenerator


class LinkGenerator:
    def __init__(self):
        self.archigator_url = os.getenv("ARCHIGATOR_URL", "http://localhost:8000")

    def generate_link(self, project_id: int):
        gitlab_api = Gitlab_API()
        project = gitlab_api.get_project(project_id)

        hmac_generator = HmacGenerator(os.getenv("ARCHIGATOR_SECRET"))
        signature = hmac_generator.generate_signature(project_id, project.name)
        link_url = hmac_generator.build_url(self.archigator_url, "main",
                                            publication=signature)
        return link_url
