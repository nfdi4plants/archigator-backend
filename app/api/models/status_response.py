from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel

from app.invenio.models.record import *


class Receipt(BaseModel):
    status: Optional[str] = None
    web_url: Optional[str] = None
    investigation_name: Optional[str] = None
    # project_name: Optional[str] = None
    # project_owner: Optional[str] = None
    comments: Optional[list] = []
    order_id: Optional[str] = None



class Test(BaseModel):
    name: str
    status: str
    system_output: str


class UserProject(BaseModel):
    name: Optional[str] = None
    web_url: Optional[str] = None
    status: Optional[str] = None
    avatar_url: Optional[str] = None


class ProjectPipeline(BaseModel):
    status: str
    finished_at: str
    web_url: str
    # details_path: str
    tests: Optional[List[Test]] = None


class Gituser(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None
    web_url: Optional[str] = None
    is_member: Optional[bool] = False
    project_url: Optional[str] = None


class Tests(BaseModel):
    __root__: Optional[List[Test]]


class StatusResponse(BaseModel):
    # pipeline_status: str
    # project_name: str
    user: Optional[Gituser] = None
    project: Optional[UserProject] = None
    pipeline: Optional[ProjectPipeline] = None
    metadata: Optional[Metadata] = None
