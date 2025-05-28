from typing import Final

import uvicorn

from stackcalc.api.env import EnvironmentVariables as ENV
from stackcalc.api.fastapi import ifc as api

HOST: Final[str] = ENV.get_host()
PORT: Final[int] = ENV.get_port()

if __name__ == "__main__":
    uvicorn.run(api, host=HOST, port=PORT)
