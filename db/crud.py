import hashlib, base64, random, string
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
from schemas import schemas
from config import LINK_NAME_LENGHT


CHARACTERS = string.ascii_letters + string.digits


async def get_links(db: AsyncSession, offset: int, limit: int):
    links = await db.execute(select(models.Link).limit(limit).offset(offset).order_by(models.Link.id))
    return links.scalars().all()


async def get_link_by_destination_url(destination_url: str, db: AsyncSession) -> models.Link:
    links = await db.execute(select(models.Link).filter_by(destination_url=destination_url))
    return links.scalars().first()


async def get_link_by_name(name: str, db: AsyncSession) -> models.Link:
    links = await db.execute(select(models.Link).filter_by(name=name))
    return links.scalars().first()


def create_hash(text: str) -> str:
    return base64.urlsafe_b64encode(
        hashlib.sha1(
            text.encode("ascii")
        ).digest()
    ).decode("ascii")[:LINK_NAME_LENGHT]


def create_salt() -> str:
    return "".join(random.sample(CHARACTERS, k=15))


async def create_link(link: schemas.LinkCreate, db: AsyncSession) -> models.Link:
    name = create_hash(text=link.destination_url)
    expires_at = datetime.now() + timedelta(days=link.days_to_expire)

    # chech for collision
    if not await get_link_by_name(name=name, db=db):
        link_db = models.Link(
            name=name, 
            destination_url=link.destination_url,
            expires_at=expires_at,
        )
        db.add(link_db)
        return link_db

    # in case of collision
    names_with_salt = {}
    for _ in range(10):
        salt = create_salt()
        name = create_hash(text=link.destination_url + salt)
        names_with_salt[name] = salt

    db_names = await db.execute(select(models.Link.name).filter(models.Link.name.in_(names_with_salt.keys())))
    db_names_set = set(db_names.scalars().all())

    for name in names_with_salt:
        if name in db_names_set:
            continue
        link_db = models.Link(
            name=name, 
            destination_url=link.destination_url,
            expires_at=expires_at,
        )
        db.add(link_db)
        return link_db
