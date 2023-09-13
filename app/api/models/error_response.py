from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Error(BaseModel):
    title: str
    detail: str
    # type: str
    code: int


class ErrorResponse(BaseModel):
    errors: Optional[List[Error]] = None
