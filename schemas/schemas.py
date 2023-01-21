from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class LinkBase(BaseModel):
    pass


class LinkCreate(LinkBase):
    days_to_expire: Optional[int] = 90
    destination_url: str


class LinkResponse(LinkBase):
    url: str
    expires_at: datetime

    class Config:
        orm_mode = True


class Link(LinkResponse):
    id: int
    name: str
    destination_url: str
    salt: Optional[str]
    created_at: datetime


    class Config:
        orm_mode = True