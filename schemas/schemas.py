from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class LinkBase(BaseModel):
    days_to_expire: Optional[int] = 90


class LinkCreate(LinkBase):
    destination_url: str


class LinkResponse(LinkBase):
    name: str

    class Config:
        orm_mode = True