from __future__ import annotations

from typing import List

from pydantic import BaseModel


class FileItem(BaseModel):
    key: str


class DraftFile(BaseModel):
    __root__: List[FileItem]
