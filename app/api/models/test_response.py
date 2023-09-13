from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class TestResponse(BaseModel):
    projectid: Optional[str] = None
    owner: str
    owner_id: str
    lfs: bool
