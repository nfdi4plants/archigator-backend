from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Status(BaseModel):
    signature: str
    project_id: int
    project_name: str

