from pydantic import BaseModel


class Input:
    class SiteCreate(BaseModel):
        name: str
        url: str
        category_id: int


class Output:
    ...