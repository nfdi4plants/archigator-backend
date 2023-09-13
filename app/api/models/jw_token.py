from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class JwtToken(BaseModel):
    project_id: int
    project_name: str

class OrderToken(BaseModel):
    project_id: int
    request_id: str

