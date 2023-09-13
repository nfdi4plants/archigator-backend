from __future__ import annotations

from typing import List, Dict, Optional

from pydantic import BaseModel


class BadgeEdit(BaseModel):
    name: str
    link_url: str
    image_url: str


class Badge(BaseModel):
    name: str
    link_url: str
    image_url: str
    rendered_link_url: Optional[str]
    rendered_image_url: Optional[str]
    id: Optional[int]
    kind: Optional[str]


class BadgeList(BaseModel):
    __root__: List[Badge]
