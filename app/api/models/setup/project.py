from __future__ import annotations

from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
    project_id: int
    overwrite: Optional[bool] = False

class Projects(BaseModel):
    overwrite: Optional[bool] = False
