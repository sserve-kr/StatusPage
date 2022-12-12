from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .engine import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    order = Column(Integer, default=0)

    sites = relationship("Site", back_populates="category")


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    order = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="sites")
    responses = relationship("Response", back_populates="site")


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    success = Column(Boolean, index=True)
    timestamp = Column(Integer, index=True)

    site_id = Column(Integer, ForeignKey("sites.id"))

    site = relationship("Site", back_populates="responses")
