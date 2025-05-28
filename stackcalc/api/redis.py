from typing import Final

import redis

from stackcalc.api.env import EnvironmentVariables as ENV

BACKEND: Final[str] = ENV.get_backend_url()

db = redis.from_url(BACKEND)
