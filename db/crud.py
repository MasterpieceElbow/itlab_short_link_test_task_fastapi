import hashlib, base64, random, string

from sqlalchemy.orm import Session

from db import models
from schemas import schemas
from config import LINK_NAME_LENGHT


CHARACTERS = string.ascii_letters + string.digits


def get_links(db: Session):
    return db.query(models.Link).all()


def get_link_by_destination_url(destination_url: str, db: Session) -> models.Link:
    return db.query(models.Link).filter_by(destination_url=destination_url).first()


def get_link_by_name(name: str, db: Session) -> models.Link:
    return db.query(models.Link).filter_by(name=name).first()


def create_name(text: str) -> str:
    return base64.urlsafe_b64encode(
        hashlib.sha1(
            text.encode("ascii")
        ).digest()
    ).decode("ascii")[:LINK_NAME_LENGHT]


def create_salt() -> str:
    return "".join(random.sample(CHARACTERS, k=15))


def create_link(link: schemas.LinkCreate, db: Session) -> models.Link:
    name = create_name(text=link.destination_url)

    # chech for collision
    if not get_link_by_name(name=name, db=db):
        link_db = models.Link(name=name, **link.dict())
        db.add(link_db)
        return link_db

    # in case of collision
    names_with_salt = {}
    for _ in range(10):
        salt = create_salt()
        name = create_name(text=link.destination_url + salt)
        names_with_salt[name] = salt

    db_names = db.query(models.Link.name).filter(models.Link.name.in_(names_with_salt.keys()))
    db_names_set = set(db.scalars(db_names).all())

    for name in names_with_salt:
        if name in db_names_set:
            continue

        link_db = models.Link(
            name=name,
            salt=names_with_salt[name],
            **link.dict(),
        )
        db.add(link_db)
        return link_db
