from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time

from db.engine import SessionLocal
from db.crud import Response


class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def add_job(self, func, trigger, args=None, kwargs=None, id=None, **trigger_args):
        self.scheduler.add_job(func, trigger, args=args, kwargs=kwargs, id=id, **trigger_args)

    def remove_job(self, job_id):
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            pass

    def shutdown(self):
        self.scheduler.shutdown()


await def uptime_robot(site_id, site_url):
    res = requests.get(site_url)
    Response().create(
        code=res.status_code,
        success=res.ok,
        response_time=res.elapsed.microseconds,
        timestamp=int(time.time()),
        site_id=site_id
    )
