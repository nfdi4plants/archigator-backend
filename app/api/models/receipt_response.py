from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Receipt(BaseModel):
    status: str
    owner: str
    project_name: str

