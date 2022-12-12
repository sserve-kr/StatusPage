from fastapi import FastAPI, APIRouter, Depends
import dependencies as dp
from sqlalchemy.orm import Session

from db import crud
from models import Input, Output

app = FastAPI()
router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/site")
async def create_site(site: Input.SiteCreate, db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Create a site"""
    if not auth:
        return Output.Error(msg="Invalid cookie")
    site = crud.Site(db).create(name=site.name, url=site.url, category_id=site.category_id)
    return Output.SiteCreate(id=site.id, name=site.name, url=site.url, category_id=site.category_id)