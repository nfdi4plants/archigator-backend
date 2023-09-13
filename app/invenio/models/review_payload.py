from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Payload(BaseModel):
    content: str = "This review was generated automatically by Archigator =^..^="
    format: str = "html"


class ReviewPayload(BaseModel):
    payload: Optional[Payload] = None
