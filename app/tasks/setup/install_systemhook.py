import os
from app.gitlab.api import Gitlab_API
from app.gitlab.models.badges import *
from app.helpers.hmac_generator import HmacGenerator
from app.gitlab.models.setup_system_hook import *
from app.helpers.token_generator import TokenGenerator


def install_systemhook(overwrite: bool = False):
    gitlab_url = os.getenv("GITLAB_URL", "http://localhost")
    archigator_url = os.getenv("ARCHIGATOR_URL", "http://localhost:8000")

    archigator_hook_url = f'{archigator_url}{"/api/v1/hooks/systemhook"}'

    gitlab_api = Gitlab_API()

    token_generator = TokenGenerator()
    # token = token_generator.generate()
    token = os.getenv("GITLAB_SECRET", "archigator")
    print("generated token", token)

    systemhook = AddSystemHook(url=archigator_hook_url, token=token, repository_update_events=True)
    print("systemhook", systemhook)

    gitlab_api.add_systemhook(systemhook)

    print("token is", token)

    return token
