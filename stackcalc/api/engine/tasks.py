import json
import time
from typing import List

from stackcalc.api.celery import celery, logger
from stackcalc.api.engine.models import Problem, Solution
from stackcalc.api.redis import db
from stackcalc.api.serializer import pydantic_dumps, pydantic_loads


@celery.task(bind=True)
def calculate(self, strategy: str, payload: str) -> str:
    task_id: str = f"{self.request.id}"
    task_key: str = f"celery-task-meta-{task_id}"
    task_data: Problem = pydantic_loads(payload)
    logger.info(f"Task: '{task_id}'")
    logger.info(f"Strategy: '{strategy}'")
    logger.info(f"Payload: {task_data}")
    res_bytes = db.get(task_key)
    res_dict = json.loads(res_bytes.decode("utf-8"))  # type: ignore
    res_dict["progress"] = 0
    logger.info(res_dict)
    for i in range(1, 101):
        time.sleep(1)
        res_dict["progress"] = i
        res_bytes = json.dumps(res_dict).encode("utf-8")
        db.set(task_key, res_bytes)
    logger.info("Done")
    task_result: Solution = Solution()
    return pydantic_dumps(task_result)
