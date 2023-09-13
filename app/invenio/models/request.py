from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel


class Receiver(BaseModel):
    community: str


class Topic(BaseModel):
    record: str


class CreatedBy(BaseModel):
    user: str


class Links(BaseModel):
    actions: Dict[str, Any]
    self: str
    comments: str
    timeline: str


class Request(BaseModel):
    number: Optional[str] = None
    receiver: Optional[Receiver] = None
    expires_at: Optional[Any] = None
    is_open: Optional[bool] = None
    type: Optional[str] = None
    status: Optional[str] = None
    is_closed: Optional[bool] = None
    topic: Optional[Topic] = None
    updated: Optional[str] = None
    created: Optional[str] = None
    is_expired: Optional[bool] = None
    created_by: Optional[CreatedBy] = None
    id: Optional[str] = None
    title: Optional[str] = None
    links: Optional[Links] = None
    revision_id: Optional[int] = None
