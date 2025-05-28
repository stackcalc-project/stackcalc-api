from typing import Final

from celery import Celery
from celery.signals import worker_shutting_down
from celery.utils.log import get_task_logger

from stackcalc.api.env import EnvironmentVariables as ENV

BROKER: Final[str] = ENV.get_broker_url()
BACKEND: Final[str] = ENV.get_backend_url()

celery = Celery(
    "stackcalc",
    backend=BACKEND,
    broker=BROKER,
    include=["stackcalc.api.engine.tasks"],
)
celery.conf.update(
    task_track_started=True,
)

# TODO: depending on the type of subscription, route differently, e.g.:
# celery.conf.task_routes = {"stackcalc.api.free_sub_task": "slow-queue"}
# celery.conf.task_routes = {"stackcalc.api.business_task": "fast-queue"}
# celery.conf.task_routes = {"stackcalc.api.enterprise_task": "dedicated-queue"}

logger = get_task_logger(__name__)


@worker_shutting_down.connect
def worker_shutting_down_handler(sig, how, exitcode, **kwargs):
    logger.info("celery worker is being shutdown, cleaning up resources...")
    pass  # something todo?
