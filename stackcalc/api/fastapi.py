from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from stackcalc.api.auth import routers as auth_routers
from stackcalc.api.engine import routers as engine_routers

STACKCALC_API_TITLE: Final[str] = "StackCalc API"

ifc = FastAPI(title=STACKCALC_API_TITLE, root_path="/api")
ifc.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ifc_v1 = FastAPI(title=STACKCALC_API_TITLE)
ifc_v1.include_router(auth_routers.router_v1)
ifc_v1.include_router(engine_routers.router_v1)

ifc_v2 = FastAPI(title=STACKCALC_API_TITLE)
ifc_v2.include_router(auth_routers.router_v2)
ifc_v2.include_router(engine_routers.router_v1)

ifc.mount("/v1", ifc_v1)
ifc.mount("/v2", ifc_v2)


@ifc.get("/")
def root():
    return {"message": "StackCalc API says hi!"}
