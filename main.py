from datetime import timedelta, datetime
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from db import crud
from db.models import Base
from db.database import engine
from db.dependencies import get_db
from schemas import schemas


Base.metadata.create_all(bind=engine)

app = FastAPI()


missing_link_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Link expired or doesn't exist"
)


@app.get("/links/", response_model=list[schemas.LinkResponse])
def get_links(db: Session = Depends(get_db)):
    return crud.get_links(db=db)


@app.post("/links/", response_model=schemas.LinkResponse)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    link_db = crud.get_link_by_destination_url(destination_url=link.destination_url, db=db)

    if not link_db:
        new_link = crud.create_link(link=link, db=db)
        db.commit()
        return new_link

    if link_db.created_at + timedelta(days=link_db.days_to_expire) > datetime.now():
        return link_db

    # if created without salt - only update created_at and days_to_expire
    if not link_db.salt:
        link_db.created_at = datetime.now()
        link_db.days_to_expire = link.days_to_expire
        db.commit()
        return link_db

    # if expired and created with salt - create the brand new one
    new_link = crud.create_link(link=link, db=db)
    db.commit()
    return new_link


@app.get("/{link_name}/", response_model=schemas.LinkResponse)
def get_link(link_name: str, db: Session = Depends(get_db)):
    link_db = crud.get_link_by_name(name=link_name, db=db)

    if not link_db or datetime.now() > link_db.created_at + timedelta(days=link_db.days_to_expire):
        raise missing_link_exception
    
    return RedirectResponse(link_db.destination_url)
