from __future__ import annotations

from pydantic import BaseModel
from typing import Optional

class Publication(BaseModel):
    user: Optional[str] = None
    project_name: Optional[str] = None
    record_id: Optional[str] = None
    order_url: Optional[str] = None
    token: Optional[str] = None
