from tomllib import load

from db.engine import SessionLocal

from fastapi import HTTPException, Query

with open("initial.toml", "rb") as f:
    cf = load(f)


async def auth(cookie: str = Query(...)) -> bool:
    """Check if the cookie is valid"""
    if cf["Auth"]["ADMIN_TOKEN"] == cookie:
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()