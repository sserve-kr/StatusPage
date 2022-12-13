from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Response
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
async def create_site(site: Input.Create.Site, db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Create a site"""
    site = crud.Site(db).create(name=site.name, url=site.url, category_id=site.category_id)
    return Output.Create.Site(id=site.id, name=site.name, url=site.url, category_id=site.category_id)


@router.get("/category")
async def get_categories(db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Get all categories"""
    categories = crud.Category(db).get_all()
    return Output.Get.CategoryList(categories=[Output.Get.Category(id=category.id, name=category.name) for category in categories])


@router.get("/category/{category_id}")
async def get_category_items(category_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Get all sites in a category"""
    category = crud.Category(db).get(query={"ID": category_id})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    sites = crud.Site(db).get_all(query={"CATEGORY_ID": category_id})
    return Output.Get.SiteList(sites=[Output.Get.Site(id=site.id, name=site.name, url=site.url, category_id=site.category_id) for site in sites])


@router.get("/site/{site_id}")
async def get_site(site_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Get a site detail"""
    site = crud.Site(db).get(query={"ID": site_id})
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    return Output.Get.Site(id=site.id, name=site.name, url=site.url, category_id=site.category_id)


@router.delete("/site/{site_id}")
async def delete_site(site_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Delete a site"""
    site = crud.Site(db).get(query={"ID": site_id})
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    crud.Site(db).delete(query={"ID": site_id})
    return Response()


@router.get("/site/{site_id}/response")
async def get_site_responses(site_id: int = Path(..., gt=0), db: Session = Depends(dp.get_db), auth: bool = Depends(dp.auth)):
    """Get all responses of a site"""
    site = crud.Site(db).get(query={"ID": site_id})
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    responses = crud.Response(db).get_all(query={"SITE_ID": site_id})
    return Output.Get.ResponseList(
        responses=[
            Output.Get.Response(
                id=response.id,
                code=response.code,
                success=response.success,
                response_time=response.response_time
            ) for response in responses
        ]
    )

app.include_router(router)
