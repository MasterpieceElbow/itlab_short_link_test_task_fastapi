import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from db.database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    destination_url = Column(String, unique=True, index=True)
    salt = Column(String, nullable=True)
    days_to_expire = Column(Integer, default=90)
    created_at = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Link id:{self.id}, name:{self.name}, dest:{self.destination_url}>"