from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Identity(BaseModel):
    provider: str
    extern_uid: str


class User(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    state: Optional[str] = None
    avatar_url: Optional[str] = None
    web_url: Optional[str] = None
    created_at: Optional[str] = None
    is_admin: Optional[bool] = None
    bio: Optional[str] = None
    location: Optional[Any] = None
    public_email: Optional[str] = None
    skype: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    discord: Optional[str] = None
    website_url: Optional[str] = None
    organization: Optional[str] = None
    job_title: Optional[str] = None
    pronouns: Optional[str] = None
    work_information: Optional[Any] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    local_time: Optional[str] = None
    last_sign_in_at: Optional[str] = None
    confirmed_at: Optional[str] = None
    theme_id: Optional[int] = None
    last_activity_on: Optional[str] = None
    color_scheme_id: Optional[int] = None
    projects_limit: Optional[int] = None
    current_sign_in_at: Optional[str] = None
    note: Optional[str] = None
    identities: Optional[List[Identity]] = None
    can_create_group: Optional[bool] = None
    can_create_project: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None
    external: Optional[bool] = None
    private_profile: Optional[bool] = None
    commit_email: Optional[str] = None
    current_sign_in_ip: Optional[str] = None
    last_sign_in_ip: Optional[str] = None
    plan: Optional[str] = None
    trial: Optional[bool] = None
    sign_in_count: Optional[int] = None
    namespace_id: Optional[int] = None
    created_by: Optional[Any] = None
