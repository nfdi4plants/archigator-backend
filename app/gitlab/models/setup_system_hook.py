from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class AddSystemHook(BaseModel):
    url: str
    token: Optional[str] = False
    push_events: Optional[bool] = False
    tag_push_events: Optional[bool] = False
    merge_requests_events: Optional[bool] = False
    repository_update_events: Optional[bool] = False
    enable_ssl_verification: Optional[bool] = True


class SystemhookSetupResponse(BaseModel):
    token: str
