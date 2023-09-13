from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Payload(BaseModel):
    content: Optional[str] = None
    format: str
    event: Optional[str] = None


class CreatedBy(BaseModel):
    user: str


class Permissions(BaseModel):
    can_update_comment: Optional[bool] = None
    can_delete_comment: Optional[bool] = None


class Links(BaseModel):
    self: str


class Hit(BaseModel):
    type: str
    updated: str
    created: str
    payload: Payload
    created_by: CreatedBy
    id: str
    permissions: Permissions
    links: Links
    revision_id: int


class Hits(BaseModel):
    hits: List[Hit]
    total: int


class Links1(BaseModel):
    self: str


class Timeline(BaseModel):
    hits: Optional[Hits] = None
    sortBy: Optional[str] = None
    links: Optional[Links1] = None
