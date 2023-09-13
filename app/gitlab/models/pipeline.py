from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    name: str
    state: str
    avatar_url: str
    web_url: str


class DetailedStatus(BaseModel):
    icon: str
    text: str
    label: str
    group: str
    tooltip: str
    has_details: bool
    details_path: str
    illustration: Any
    favicon: str


class Pipeline(BaseModel):
    id: Optional[int] = None
    iid: Optional[int] = None
    project_id: Optional[int] = None
    sha: Optional[str] = None
    ref: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    web_url: Optional[str] = None
    before_sha: Optional[str] = None
    tag: Optional[bool] = None
    yaml_errors: Optional[Any] = None
    user: Optional[User] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    committed_at: Optional[Any] = None
    duration: Optional[int] = None
    queued_duration: Optional[int] = None
    coverage: Optional[Any] = None
    detailed_status: Optional[DetailedStatus] = None
