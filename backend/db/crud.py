from sqlalchemy.orm import Session
import time

from . import models


class Site:
    ID = (int, "id")
    NAME = (str, "name")
    URL = (str, "url")
    IS_ACTIVE = (bool, "is_active")
    ORDER = (int, "order")
    CATEGORY_ID = (int, "category_id")

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def type_check(query: dict):
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)

    def get(self, query: dict = None) -> models.Site:
        if not query:
            query = {}
        self.type_check(query)
        
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Site).filter_by(**query).first()

    def get_all(self, query: dict = None) -> list[models.Site]:
        if not query:
            query = {}
        self.type_check(query)
        
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Site).filter_by(**query).all()

    def create(self, **fields) -> models.Site:
        
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in fields.items() if (cur := type(value)) != (exp := getattr(models.Site.CreateRequiredFields, attr))]:
            raise ExceptionGroup("Invalid Field Types", type_errs)
        site = models.Site(**fields)
        self.db.add(site)
        self.db.commit()
        self.db.refresh(site)
        return site

    def delete(self, query: dict):
        self.get(query).delete()
        self.db.commit()

    def update(self, site_id: int, **fields):
        
        site = self.get({self.ID: site_id})
        for attr, value in fields.items():
            setattr(site, attr, value)
        self.db.commit()
        self.db.refresh(site)
        return site


class Category:
    ID = (int, "id")
    NAME = (str, "name")
    ORDER = (int, "order")

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def type_check(query: dict):
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)

    def get(self, query: dict = None) -> models.Category:
        if not query:
            query = {}
        self.type_check(query)
        
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Category).filter_by(**query).first()

    def get_all(self, query: dict = None) -> list[models.Category]:
        if not query:
            query = {}
        self.type_check(query)
        
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Category).filter_by(**query).all()

    def create(self, **fields) -> models.Category:
        
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in fields.items() if (cur := type(value)) != (exp := getattr(models.Category.CreateRequiredFields, attr))]:
            raise ExceptionGroup("Invalid Field Types", type_errs)
        category = models.Category(**fields)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int):
        
        category = self.get({self.ID: category_id})
        self.db.delete(category)
        self.db.commit()

    def update(self, category_id: int, **fields):
        
        category = self.get({self.ID: category_id})
        for attr, value in fields.items():
            setattr(category, attr, value)
        self.db.commit()
        self.db.refresh(category)
        return category


class Response:
    ID = (int, "id")
    SITE_ID = (int, "site_id")
    CODE = (int, "code")
    SUCCESS = (bool, "success")
    RESPONSE_TIME = (int, "response_time")
    TIMESTAMP = (int, "timestamp")

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def type_check(query: dict):
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)

    def get(self, query: dict = None) -> models.Response:
        if not query:
            query = {}
        self.type_check(query)
        
        query = {attr[1]: value for attr, value in query.items()}
        return self.db.query(models.Response).filter_by(**query).first()

    def get_all(self, query: dict = None, limit: int = None) -> list[models.Response]:
        if not query:
            query = {}
        self.type_check(query)
        
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in query.items() if (cur := type(value)) != (exp := attr[0])]:
            raise ExceptionGroup("Invalid Query Types", type_errs)
        query = {attr[1]: value for attr, value in query.items()}
        if limit:
            return self.db.query(models.Response).filter_by(**query).limit(limit).all()
        return self.db.query(models.Response).filter_by(**query).all()

    def create(self, **fields) -> models.Response:
        
        if type_errs := [TypeError(f"{cur}, not {exp}") for attr, value in fields.items() if (cur := type(value)) != (exp := getattr(models.Response.CreateRequiredFields, attr))]:
            raise ExceptionGroup("Invalid Field Types", type_errs)
        response = models.Response(**fields)
        self.db.add(response)
        self.db.commit()
        self.db.refresh(response)
        return response

    def delete(self, query: dict):
        self.get(query).delete()
        self.db.commit()

    def delete_old(self, days=None, weeks=None, months=None):
        t = 7 * 24 * 60 * 60 # default - 7 days
        if days:
            t = days * 24 * 60 * 60
        elif weeks:
            t = weeks * 7 * 24 * 60 * 60
        elif months:
            t = months * 30 * 24 * 60 * 60
        self.db.query(models.Response).filter(
            models.Response.timestamp < int(time.time()) - t
        ).delete()
        self.db.commit()
