from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Versions(BaseModel):
    is_latest_draft: bool
    index: int
    is_latest: bool


class OwnedByItem(BaseModel):
    user: int


class Access(BaseModel):
    owned_by: List[OwnedByItem]
    links: List


class Parent(BaseModel):
    communities: Dict[str, Any]
    id: str
    access: Access


class Files(BaseModel):
    enabled: bool
    order: List


class PersonOrOrg(BaseModel):
    type: str
    given_name: str
    family_name: str
    name: str


class Creator(BaseModel):
    person_or_org: PersonOrOrg


class Title(BaseModel):
    en: str


class ResourceType(BaseModel):
    id: str
    title: Title


class Metadata(BaseModel):
    title: str
    creators: List[Creator]
    publication_date: str
    resource_type: ResourceType


class Links(BaseModel):
    self: str
    self_html: str
    self_iiif_manifest: str
    self_iiif_sequence: str
    files: str
    record: str
    record_html: str
    publish: str
    review: str
    versions: str
    access_links: str
    reserve_doi: str


class Embargo(BaseModel):
    active: bool
    reason: Any


class Access1(BaseModel):
    record: str
    status: str
    files: str
    embargo: Embargo


class Draft(BaseModel):
    expires_at: Optional[str] = None
    status: Optional[str] = None
    versions: Optional[Versions] = None
    updated: Optional[str] = None
    parent: Optional[Parent] = None
    created: Optional[str] = None
    files: Optional[Files] = None
    metadata: Optional[Metadata] = None
    id: Optional[str] = None
    is_draft: Optional[bool] = None
    pids: Optional[Dict[str, Any]] = None
    is_published: Optional[bool] = None
    links: Optional[Links] = None
    revision_id: Optional[int] = None
    access: Optional[Access1] = None
