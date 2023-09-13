from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    description: Any
    web_url: str
    avatar_url: Any
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: Any
    homepage: str
    url: str
    ssh_url: str
    http_url: str


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
    added: List
    modified: List[str]
    removed: List


class Repository(BaseModel):
    name: str
    url: str
    description: Any
    homepage: str
    git_http_url: str
    git_ssh_url: str
    visibility_level: int


class SystemHook_Push(BaseModel):
    object_kind: Optional[str] = None
    event_name: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    ref: Optional[str] = None
    checkout_sha: Optional[str] = None
    message: Optional[Any] = None
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    user_username: Optional[str] = None
    user_email: Optional[str] = None
    user_avatar: Optional[str] = None
    project_id: Optional[int] = None
    project: Optional[Project] = None
    commits: Optional[List[Commit]] = None
    total_commits_count: Optional[int] = None
    push_options: Optional[Dict[str, Any]] = None
    repository: Optional[Repository] = None
