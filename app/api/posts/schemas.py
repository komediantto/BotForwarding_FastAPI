from typing import List, Optional

from pydantic import BaseModel


class MediaCreate(BaseModel):
    path: str


class PostCreate(BaseModel):
    text: Optional[str]
    mediafiles: Optional[List[str]]
    target: int
