from pydantic import BaseModel


class Base(BaseModel):
    error: bool


class Input:
    class SiteCreate(Base):
        name: str
        url: str
        category_id: int


class Output:
    ...
