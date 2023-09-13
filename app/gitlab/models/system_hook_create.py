from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Owner(BaseModel):
    name: str
    email: str


class SystemHookCreate(BaseModel):
    event_name: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    path: Optional[str] = None
    path_with_namespace: Optional[str] = None
    project_id: Optional[int] = None
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    owners: Optional[List[Owner]] = None
    project_visibility: Optional[str] = None
