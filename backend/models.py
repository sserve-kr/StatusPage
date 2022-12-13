from pydantic import BaseModel


class Base(BaseModel):
    error: bool


class Category(Base):
    id: int
    name: str


class Response(Base):
    id: int
    code: int
    success: bool
    response_time: float


class Site(Base):
    id: int
    name: str
    url: str
    category_id: int


class Input:
    class Create:
        class Site(Base):
            name: str
            url: str
            category_id: int


class Output:
    class Create:
        class Site(Base):
            id: int
            name: str
            url: str
            category_id: int

    class Get:
        class Category(Base):
            id: int
            name: str

        class CategoryList(Base):
            categories: list[Category]

        class Site(Base):
            id: int
            name: str
            url: str
            category_id: int

        class SiteList(Base):
            sites: list[Site]

        class Response(Base):
            id: int
            code: int
            success: bool
            response_time: float

        class ResponseList(Base):
            responses: list[Response]
