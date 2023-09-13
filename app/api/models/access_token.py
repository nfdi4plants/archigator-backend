from __future__ import annotations

from typing import Any, List, Optional, Union

from pydantic import BaseModel

class AccessToken(BaseModel):
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: str