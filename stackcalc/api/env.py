import os


class EnvironmentVariables:

    @staticmethod
    def get_host() -> str:
        return os.getenv("STACKCALC_API_HOST")  # type: ignore

    @staticmethod
    def get_port() -> int:
        return int(os.getenv("STACKCALC_API_PORT"))  # type: ignore

    @staticmethod
    def get_broker_url() -> str:
        return os.getenv("STACKCALC_API_BROKER_URL")  # type: ignore

    @staticmethod
    def get_worker_taskname() -> str:
        return os.getenv("STACKCALC_API_WORKER_TASKNAME")  # type: ignore

    @staticmethod
    def get_backend_url() -> str:
        return os.getenv("STACKCALC_API_BACKEND_URL")  # type: ignore
