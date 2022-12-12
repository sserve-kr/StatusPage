from sqlalchemy.orm import Session

from . import models
from .engine import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Site:
    ID = (int, models.Site.id)
    NAME = (str, models.Site.name)
    URL = (str, models.Site.url)
    IS_ACTIVE = (bool, models.Site.is_active)
    ORDER = (int, models.Site.order)

    def __init__(self, db: Session = None):
        self.db = db

    @staticmethod
    def type_check(query: dict):
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)

    def db_check(self):
        if not self.db:
            self.db = get_db()

    def get(self, query: dict) -> models.Site:
        self.type_check(query)
        self.db_check()
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Site).filter_by(**query).first()

    def get_all(self, query: dict) -> list[models.Site]:
        self.type_check(query)
        self.db_check()
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Site).filter_by(**query).all()

    def create(self, **fields) -> models.Site:
        self.db_check()
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in fields.items() if (cur := type(value)) != (exp := getattr(models.Site.CreateRequiredFields, attr))]:
            raise ExceptionGroup("Invalid Field Types", type_errs)
        site = models.Site(**fields)
        self.db.add(site)
        self.db.commit()
        self.db.refresh(site)
        return site

    def delete(self, site_id: int):
        self.db_check()
        site = self.get({self.ID: site_id})
        self.db.delete(site)
        self.db.commit()

    def update(self, site_id: int, **fields):
        self.db_check()
        site = self.get({self.ID: site_id})
        for attr, value in fields.items():
            setattr(site, attr, value)
        self.db.commit()
        self.db.refresh(site)
        return site


class Category:
    ID = (int, models.Category.id)
    NAME = (str, models.Category.name)
    ORDER = (int, models.Category.order)

    def __init__(self, db: Session = None):
        self.db = db

    def db_check():
        if not self.db:
            self.db = get_db()

    @staticmethod
    def type_check(query: dict):
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)

    def get(self, query: dict) -> models.Category:
        self.type_check(query)
        self.db_check()
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Category).filter_by(**query).first()

    def get_all(self, query: dict) -> list[models.Category]:
        self.type_check(query)
        self.db_check()
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Category).filter_by(**query).all()

    def create(self, **fields) -> models.Category:
        self.db_check()
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in fields.items() if (cur := type(value)) != (exp := getattr(models.Category.CreateRequiredFields, attr))]:
            raise ExceptionGroup("Invalid Field Types", type_errs)
        category = models.Category(**fields)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int):
        self.db_check()
        category = self.get({self.ID: category_id})
        self.db.delete(category)
        self.db.commit()

    def update(self, category_id: int, **fields):
        self.db_check()
        category = self.get({self.ID: category_id})
        for attr, value in fields.items():
            setattr(category, attr, value)
        self.db.commit()
        self.db.refresh(category)
        return category


class Response:
    ID = (int, models.Response.id)
    SITE_ID = (int, models.Response.site_id)
    CATEGORY_ID = (int, models.Response.category_id)
    RESPONSE = (str, models.Response.response)
    IS_ACTIVE = (bool, models.Response.is_active)
    ORDER = (int, models.Response.order)

    def __init__(self, db: Session = None):
        self.db = db

    def db_check():
        if not self.db:
            self.db = get_db()

    @staticmethod
    def type_check(query: dict):
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)

    def get(self, query: dict) -> models.Response:
        self.type_check(query)
        self.db_check()
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Response).filter_by(**query).first()

    def get_all(self, query: dict) -> list[models.Response]:
        self.type_check(query)
        self.db_check()
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Response).filter_by(**query).all()

    def create(self, **fields) -> models.Response:
        self.db_check()
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in fields.items() if (cur := type(value)) != (exp := getattr(models.Response.CreateRequiredFields, attr))]:
            raise ExceptionGroup("Invalid Field Types", type_errs)
        response = models.Response(**fields)
        self.db.add(response)
        self.db.commit()
        self.db.refresh(response)
        return response
