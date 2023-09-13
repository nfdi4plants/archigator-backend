from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    description: str
    web_url: str
    avatar_url: str
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str


class Author(BaseModel):
    name: str
    email: str


class Commit(BaseModel):
    id: str
    message: str
    title: str
    timestamp: str
    url: str
    author: Author


class Ci(BaseModel):
    skip: bool


class PushOptions(BaseModel):
    ci: Ci


class SystemHook(BaseModel):
    object_kind: Optional[str] = None
    event_name: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    ref: Optional[str] = None
    checkout_sha: Optional[str] = None
    message: Optional[str] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_avatar: Optional[str] = None
    project_id: Optional[int] = None
    project: Optional[Project] = None
    commits: Optional[List[Commit]] = None
    total_commits_count: Optional[int] = None
    push_options: Optional[PushOptions] = None
