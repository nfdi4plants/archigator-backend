import os
from app.gitlab.api import Gitlab_API
from app.gitlab.models.badges import *
from app.helpers.hmac_generator import HmacGenerator


def setup_project(project_id: int, overwrite: bool = False):
    gitlab_url = os.getenv("GITLAB_URL", "http://localhost")
    archigator_url = os.getenv("ARCHIGATOR_URL", "http://localhost:8000")

    preinstall_badges = ["pipeline-badge", "publish-badge"]

    print("in setup project", project_id)
    gitlab_api = Gitlab_API()

    project = gitlab_api.get_project(project_id)

    # get project badges
    badge_list = gitlab_api.list_badges(project_id)
    print("list", badge_list.__root__)

    available_badges = []

    for badge in badge_list.__root__:
        print(badge.name)
        # badges.append((badge.name, badge.id))
        if badge.name in preinstall_badges:
            print("found available badge", badge.name)
            available_badges.append(badge)
            preinstall_badges.remove(badge.name)

    # overwrite badges
    if overwrite:
        print("in overwrite")
        for badge in available_badges:
            print(available_badges)
            if badge.name == "pipeline-badge":
                link_url = f'{gitlab_url}{"/%{project_path}/commits/%{default_branch}"}'
                image_url = f'{gitlab_url}{"/%{project_path}/badges/%{default_branch}/pipeline.svg"}'
                badge_data = BadgeEdit(name=badge.name, link_url=link_url, image_url=image_url)
                gitlab_api.edit_badge(project_id, badge.id, badge_data)
            if badge.name == "publish-badge":
                hmac_generator = HmacGenerator(os.getenv("ARCHIGATOR_SECRET"))
                signature = hmac_generator.generate_signature(project_id, project.name)

                link_url = hmac_generator.build_url(archigator_url, "main",
                                                    publication=signature)
                badge_data = BadgeEdit(name=badge.name, link_url=link_url,
                                       image_url="https://img.shields.io/badge/Publish_ARC-blue?logo=gitlab&logoColor=%234FB3D9")
                gitlab_api.edit_badge(project_id, badge.id, badge_data)

    print(preinstall_badges)

    # add badges
    for preinstall_badge in preinstall_badges:
        if preinstall_badge == "pipeline-badge":
            link_url = f'{gitlab_url}{"/%{project_path}/commits/%{default_branch}"}'
            image_url = f'{gitlab_url}{"/%{project_path}/badges/%{default_branch}/pipeline.svg"}'
            badge_data = BadgeEdit(name=preinstall_badge, link_url=link_url, image_url=image_url)
            gitlab_api.add_badge(project_id, badge_data)

        if preinstall_badge == "publish-badge":
            hmac_generator = HmacGenerator(os.getenv("ARCHIGATOR_SECRET"))
            signature = hmac_generator.generate_signature(project_id, project.name)

            link_url = hmac_generator.build_url(archigator_url, "main",
                                                publication=signature)
            badge_data = BadgeEdit(name=preinstall_badge, link_url=link_url,
                                   image_url="https://img.shields.io/badge/Publish_ARC-blue?logo=gitlab&logoColor=%234FB3D9")
            gitlab_api.add_badge(project_id, badge_data)
