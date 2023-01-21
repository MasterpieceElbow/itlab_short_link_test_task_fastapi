from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Response, status, Query
from fastapi.responses import RedirectResponse

from db import crud
from db.models import Base
from db.database import engine
from db.dependencies import get_db
from schemas import schemas
from config import MAX_DAYS_TO_EXPIRE, MIN_DAYS_TO_EXPIRE


Base.metadata.create_all(bind=engine)

app = FastAPI()


missing_link_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Link expired or doesn't exist"
)


@app.get("/links/", response_model=list[schemas.Link])
def get_links(
        limit: int = Query(default=100),
        offset: int = Query(default=0), 
        db: Session = Depends(get_db),
):
    return crud.get_links(db=db, limit=limit, offset=offset)


@app.get("/{link_name}/", response_model=schemas.LinkResponse)
def get_link(link_name: str, db: Session = Depends(get_db)):
    link_db = crud.get_link_by_name(name=link_name, db=db)

    if not link_db or datetime.now() > link_db.expires_at:
        raise missing_link_exception
    
    return RedirectResponse(link_db.destination_url)


@app.post("/links/", response_model=schemas.LinkResponse, status_code=status.HTTP_201_CREATED)
def create_link(
    link: schemas.LinkCreate, 
    response: Response,
    db: Session = Depends(get_db)
):
    if not MIN_DAYS_TO_EXPIRE <= link.days_to_expire <= MAX_DAYS_TO_EXPIRE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Days to expire should be in 1 - 365 interval",
        )

    link_db = crud.get_link_by_destination_url(destination_url=link.destination_url, db=db)

    if not link_db:
        new_link = crud.create_link(link=link, db=db)
        db.commit()
        return new_link

    if link_db.expires_at > datetime.now():
        response.status_code = status.HTTP_200_OK
        return link_db

    # if expired - only update created_at and expires_at
    # expired link is inaccessible unless it was recreated
    now = datetime.now()
    link_db.created_at = now
    link_db.expires_at = now + timedelta(days=link.days_to_expire)
    db.commit()
    return link_db
