from __future__ import annotations

from pydantic import BaseModel
from typing import Optional, List


class Project(BaseModel):
    project_id: int
    overwrite: Optional[bool] = False

class Projects(BaseModel):
    overwrite: Optional[bool] = False

class TestMail(BaseModel):
    receiver: List[str]
    username: str
    projectname: str
    submission_url: str