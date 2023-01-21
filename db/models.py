import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    String,
    DateTime,
)

from db.database import Base
from config import DOMAIN_ADDRESS


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    destination_url = Column(String, unique=True, index=True)
    salt = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    expires_at = Column(DateTime)

    __table_args__ = (
        CheckConstraint("expires_at > created_at", "chech_time"),
    )

    @property
    def url(self):
        return f"{DOMAIN_ADDRESS}{self.name}"

    def __repr__(self):
        return f"<Link id:{self.id}, name:{self.name}, dest:{self.destination_url}>"
