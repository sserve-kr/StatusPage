from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
import logging
logging.basicConfig(level=logging.INFO)

from db.crud import Response, Site
from db.engine import SessionLocal


def uptime_robot(site_id, site_url):
    db = SessionLocal()
    res = requests.get(site_url)
    logging.info(f"Robot log: {site_url} {res.status_code} {'OK' if res.ok else 'ERROR'}")
    Response(db).create(
        code=res.status_code,
        success=res.ok,
        response_time=int(res.elapsed.microseconds/1000),
        timestamp=int(time.time()),
        site_id=site_id
    )
    db.close()


def lately_cleaner():
    db = SessionLocal()
    logging.info(f"Cleaner log: {len(Site(db).get_all())} sites")
    Response(db).delete_old(weeks=1)
    db.close()


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def init_from_db(self):
        db = SessionLocal()
        [self.add_robot(site_id=site.id, site_url=site.url) for site in Site(db).get_all()]
        db.close()

    def add_robot(self, **kwargs):
        logging.info(f"Added robot for {kwargs['site_url']}")
        self.scheduler.add_job(uptime_robot, kwargs=kwargs, trigger="interval", seconds=180, id=str(kwargs["site_id"]))

    def remove_robot(self, site_id):
        logging.info(f"Removed robot for {site_id}")
        try:
            self.scheduler.remove_job(site_id)
        except JobLookupError:
            pass

    def shutdown(self):
        self.scheduler.shutdown()


scheduler = Scheduler()
