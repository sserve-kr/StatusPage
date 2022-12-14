from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Response, Query
from fastapi.middleware.cors import CORSMiddleware
import dependencies as dp
from sqlalchemy.orm import Session
from typing import List

from db import crud, engine
from models import *
from robot import scheduler

app = FastAPI()
router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

engine.Base.metadata.create_all(bind=engine.engine)
scheduler.init_from_db()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://status.sserve.work",
    "https://status.sserve.work"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.get("/auth")
async def try_auth(auth: bool = Depends(dp.auth)):
    return {"success": auth}


@router.post("/category", response_model=Category)
async def create_category(category: CategoryCreate, db: Session = Depends(dp.get_db)):  # temporary disabled auth
    """Create a new category"""
    return crud.Category(db).create(**category.dict())


@router.post("/site", response_model=Site)
async def create_site(site: SiteCreate, db: Session = Depends(dp.get_db)):  # temporary disabled auth : auth: bool = Depends(dp.auth)
    """Create a site"""
    site = crud.Site(db).create(**site.dict())
    scheduler.add_robot(site_id=site.id, site_url=site.url)
    return site


@router.get("/category", response_model=List[Category])
async def get_categories(db: Session = Depends(dp.get_db)):
    """Get all categories"""
    return crud.Category(db).get_all()


@router.get("/category/{category_id}", response_model=List[Site])
async def get_category_items(category_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db)):
    """Get all sites in a category"""
    category = crud.Category(db).get(query={crud.Category.ID: category_id})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.Site(db).get_all(query={crud.Site.CATEGORY_ID: category_id})


@router.get("/site/{site_id}", response_model=Site)
async def get_site(site_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db)):
    """Get a site detail"""
    site = crud.Site(db).get(query={crud.Site.ID: site_id})
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return site


@router.delete("/site/{site_id}")
async def delete_site(site_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db)):
    """Delete a site"""
    site = crud.Site(db).get(query={crud.Site.ID: site_id})
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    crud.Site(db).delete(query={crud.Site.ID: site_id})
    crud.Response(db).delete_all(query={crud.Response.SITE_ID: site_id})
    scheduler.remove_robot(site_id=str(site_id))
    return {"success": True}


@router.get("/site/{site_id}/response", response_model=List[Response])
async def get_site_responses(site_id: int = Path(..., gt=0), limit: int = Query(...), db: Session = Depends(dp.get_db)):
    """Get all responses of a site"""
    site = crud.Site(db).get(query={crud.Site.ID: site_id})
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return crud.Response(db).get_all(query={crud.Response.SITE_ID: site_id}, limit=limit)

app.include_router(router)
