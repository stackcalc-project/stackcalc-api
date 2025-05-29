import json
from typing import Annotated, Final

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException

from stackcalc.api.celery import celery
from stackcalc.api.engine.models import (
    Job,
    MixedOptions,
    MixedProblem,
    MonoOptions,
    MonoProblem,
    Problem,
    RainbowOptions,
    RainbowProblem,
    Strategy,
)
from stackcalc.api.env import EnvironmentVariables as ENV
from stackcalc.api.redis import db
from stackcalc.api.serializer import pydantic_dumps

WORKER_TASK: Final[str] = ENV.get_worker_taskname()
router_v1 = APIRouter()


def check_problem_description(
    data: Problem,
    expected_strategy: Strategy,
    expected_strategy_options: type,
) -> Problem:
    if data.strategy != expected_strategy:
        raise HTTPException(status_code=422, detail="Invalid strategy")
    if not isinstance(data.strategy_options, expected_strategy_options):
        raise HTTPException(status_code=422, detail="Invalid strategy options")
    return data


async def check_mono(data: MonoProblem) -> Problem:
    return check_problem_description(data, Strategy.MONO, MonoOptions)


async def check_rainbow(data: RainbowProblem) -> Problem:
    return check_problem_description(data, Strategy.RAINBOW, RainbowOptions)


async def check_mixed(data: MixedProblem) -> Problem:
    return check_problem_description(data, Strategy.MIXED, MixedOptions)


@router_v1.post(
    "/jobs/mono-stack",
    tags=["engine"],
    summary="Create Mono-Stack Job",
    description="Creates a job to calculate one or more stack(s) that consists of a single item.",
)
async def create_job_mono_stack(data: Annotated[MonoProblem, Depends(check_mono)]) -> Job:
    name = WORKER_TASK
    args = [data.strategy, pydantic_dumps(data)]
    task = celery.send_task(name, args)
    return Job(id=task.task_id, status=task.status, progress=0, result=None)


@router_v1.post(
    "/jobs/rainbow-stack",
    tags=["engine"],
    summary="Create Rainbow-Stack Job",
    description="Creates a job to calculate one or more stack(s) that consists of layers each with a single item.",
)
async def create_job_rainbow_stack(data: Annotated[RainbowProblem, Depends(check_rainbow)]) -> Job:
    name = WORKER_TASK
    args = [data.strategy, pydantic_dumps(data)]
    task = celery.send_task(name, args)
    return Job(id=task.task_id, status=task.status, progress=0, result=None)


@router_v1.post(
    "/jobs/mixed-stack",
    tags=["engine"],
    summary="Create Mixed-Stack Job",
    description="Creates a job to calculate one or more stack(s) that consists (of layers) of multiple items.",
)
async def create_job_mixed_stack(data: Annotated[MixedProblem, Depends(check_mixed)]) -> Job:
    name = WORKER_TASK
    args = [data.strategy, pydantic_dumps(data)]
    task = celery.send_task(name, args)
    return Job(id=task.task_id, status=task.status, progress=0, result=None)


@router_v1.get("/jobs/{job_id}", tags=["engine"])
def get_job(job_id: str) -> Job:
    result = AsyncResult(job_id, app=celery)
    if result is None:
        raise HTTPException(status_code=404, detail="The job is unknown")
    if result.failed():
        raise HTTPException(status_code=500, detail=str(result.result))
    db_value = db.get(f"celery-task-meta-{job_id}")
    if db_value is None:
        return Job(id=job_id, status="PENDING", progress=0, result=None)
    json_value = json.loads(db_value.decode("utf-8"))  # type: ignore
    return Job(
        id=job_id,
        status=json_value["status"],
        progress=100 if result.ready() else int(json_value["progress"]),
        result=str(result.get()) if result.ready() else None,
    )


@router_v1.delete("/jobs/{job_id}", tags=["engine"])
def delete_job(job_id: str) -> Job:
    result = AsyncResult(job_id, app=celery)
    if result is None:
        raise HTTPException(status_code=404, detail="The job is unknown")
    result.forget()
    return Job(id=job_id, status="DELETED", progress=0, result=None)
