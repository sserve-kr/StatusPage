from hashlib import sha256
from tomllib import load

from db.engine import SessionLocal

with open("initial.toml", "r", encoding="utf-8") as f:
    cf = load(f)


async def auth(cookie: str) -> bool:
    """Check if the cookie is valid"""
    a = sha256(cf["ADMIN_PASS"].encode()).hexdigest()
    b = sha256(a+cf["ADMIN_USER"].encode()).hexdigest()
    c = sha256(b+cf["SECRET_KEY"].encode()).hexdigest()
    return c == cookie


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()