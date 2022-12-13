from pydantic import BaseModel


class ItemBase(BaseModel):
    class Config:
        orm_mode = True


class Category(ItemBase):
    id: int
    name: str
    order: int


class CategoryCreate(ItemBase):
    name: str
    order: int


class Site(ItemBase):
    id: int
    name: str
    url: str
    category_id: int
    order: int
    is_active: bool


class SiteCreate(ItemBase):
    name: str
    url: str
    category_id: int
    order: int
    is_active: bool


class Response(ItemBase):
    id: int
    code: int
    success: bool
    response_time: float


class ResponseList(ItemBase):
    responses: list[Response]