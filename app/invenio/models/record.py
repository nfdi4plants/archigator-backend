from __future__ import annotations

import os
from typing import List, Optional

from pydantic import BaseModel

from datetime import date


class Access(BaseModel):
    record: str = "public"
    files: str = "public"


class Files(BaseModel):
    enabled: bool = False
    default_preview: str = "arc-summary.md"
    order: Optional[list]


class ResourceType(BaseModel):
    id: str


class Identifier(BaseModel):
    scheme: str
    identifier: str


class PersonOrOrg(BaseModel):
    type: str
    name: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    identifiers: Optional[List[Identifier]]


class Affiliation(BaseModel):
    name: str


class Creator(BaseModel):
    person_or_org: PersonOrOrg
    affiliations: Optional[List[Affiliation]]


class Metadata(BaseModel):
    resource_type: Optional[ResourceType] = None
    creators: Optional[List[Creator]] = None
    title: Optional[str] = None
    description: Optional[str] = None
    # publication_date: Optional[str] = None
    publication_date: Optional[str] = date.today().isoformat()
    publisher: Optional[str] = os.environ.get("publisher", "DataPLANT")
    publication_server: Optional[str] = os.environ.get("publication_server", "https://archive.nfdi4plants.org")
    identifiers: Optional[List[Identifier]] = None


class Record(BaseModel):
    access: Optional[Access] = None
    files: Optional[Files] = None
    metadata: Optional[Metadata] = None


    def add_something(self, something):
        pass



# class Metadata(BaseModel):
#     creators: Optional[List[Creator]] = None
#     publication_date: Optional[str] = None
#     resource_type: Optional[ResourceType] = None
#     title: Optional[str] = None
#     publisher: Optional[str] = "Nfdi4plants / DataPLANT"