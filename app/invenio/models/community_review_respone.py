from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel


class CreatedBy(BaseModel):
    user: str


class Actions(BaseModel):
    submit: str


class Links(BaseModel):
    actions: Actions
    comments: str
    self: str
    timeline: str


class Receiver(BaseModel):
    community: str


class Topic(BaseModel):
    record: str


class CommunityReview(BaseModel):
    created: Optional[str] = None
    created_by: Optional[CreatedBy] = None
    expires_at: Optional[Any] = None
    id: Optional[str] = None
    is_closed: Optional[bool] = None
    is_expired: Optional[bool] = None
    is_open: Optional[bool] = None
    links: Optional[Links] = None
    number: Optional[str] = None
    receiver: Optional[Receiver] = None
    revision_id: Optional[int] = None
    status: Optional[str] = None
    title: Optional[str] = None
    topic: Optional[Topic] = None
    type: Optional[str] = None
    updated: Optional[str] = None
