import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends, HTTPException, Response, status, Query
from fastapi.responses import RedirectResponse

from db import crud
from db.database import init_models
from db.dependencies import get_db

from schemas import schemas
from config import MAX_DAYS_TO_EXPIRE, MIN_DAYS_TO_EXPIRE


asyncio.get_event_loop().create_task(init_models())

app = FastAPI()


missing_link_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Link expired or doesn't exist"
)


@app.get("/links/", response_model=list[schemas.Link])
async def get_links(
        limit: int = Query(default=100),
        offset: int = Query(default=0), 
        db: AsyncSession = Depends(get_db),
):
    return await crud.get_links(db=db, limit=limit, offset=offset)


@app.get("/{link_name}/", response_model=schemas.LinkResponse)
async def get_link(link_name: str, db: AsyncSession = Depends(get_db)):
    link_db = await crud.get_link_by_name(name=link_name, db=db)

    if not link_db or datetime.now() > link_db.expires_at:
        raise missing_link_exception
    
    return RedirectResponse(link_db.destination_url)


@app.post("/links/", response_model=schemas.LinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(
    link: schemas.LinkCreate, 
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    if not MIN_DAYS_TO_EXPIRE <= link.days_to_expire <= MAX_DAYS_TO_EXPIRE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Days to expire should be in {MIN_DAYS_TO_EXPIRE} - {MAX_DAYS_TO_EXPIRE} interval",
        )

    link_db = await crud.get_link_by_destination_url(destination_url=link.destination_url, db=db)

    if not link_db or link_db.expires_at < datetime.now():
        new_link = await crud.create_link(link=link, db=db)
        await db.commit()
        return new_link

    # if link is already created and isn't expired - return it
    response.status_code = status.HTTP_200_OK
    return link_db
