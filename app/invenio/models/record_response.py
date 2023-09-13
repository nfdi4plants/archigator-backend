from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Embargo(BaseModel):
    reason: Any
    active: bool


class Access(BaseModel):
    record: str
    files: str
    embargo: Embargo


class Files(BaseModel):
    enabled: bool


class Links(BaseModel):
    latest: str
    versions: str
    self_html: str
    publish: str
    latest_html: str
    self: str
    files: str
    access_links: str


class Title(BaseModel):
    en: str


class ResourceType(BaseModel):
    id: str
    title: Title


class Identifier(BaseModel):
    scheme: str
    identifier: str


class PersonOrOrg(BaseModel):
    family_name: str
    given_name: str
    type: str
    identifiers: Optional[List[Identifier]] = None
    name: Optional[str] = None


class Affiliation(BaseModel):
    id: str
    name: str


class Creator(BaseModel):
    person_or_org: PersonOrOrg
    affiliations: Optional[List[Affiliation]] = None


class Metadata(BaseModel):
    resource_type: ResourceType
    title: str
    publication_date: str
    creators: List[Creator]


class User(BaseModel):
    userid: str


class OwnedByItem(BaseModel):
    user: User


class Access1(BaseModel):
    owned_by: List[OwnedByItem]
    links: List


class Parent(BaseModel):
    id: str
    access: Access1


class Versions(BaseModel):
    index: int
    is_latest: bool
    is_latest_draft: bool


class RecordResponse(BaseModel):
    access: Optional[Access] = None
    created: Optional[str] = None
    expires_at: Optional[str] = None
    files: Optional[Files] = None
    id: Optional[str] = None
    is_published: Optional[bool] = None
    links: Optional[Links] = None
    metadata: Optional[Metadata] = None
    parent: Optional[Parent] = None
    pids: Optional[Dict[str, Any]] = None
    revision_id: Optional[int] = None
    updated: Optional[str] = None
    versions: Optional[Versions] = None
