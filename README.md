<img src="https://github.com/stackcalc-project/stackcalc-api/blob/main/logo.png" align="right" width="60px" height="60px"/>

# stackcalc-api

The stackcalc open source API and celery worker.

## Features

- Authentication and authorization with `oauth2`
- Calculation fully anonymous (i.e. no end-customer data required)
- Long-running tasks with flexible distributed queue system based on `celery`

## Requirements

- [python](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/)
- [podman](https://podman.io/) and/or [docker](https://www.docker.com/)
- [vscode](https://code.visualstudio.com/)
- [tiny-rdm](https://github.com/tiny-craft/tiny-rdm) (or tool to access the `redis` database)

## Usage

**running**

The quickest way to get started is by running the following one-liner. This starts the necessary services, runs the api and a single worker:

```bash
podman-compose --file docker/compose.yaml up
```

For a slighly more advanced situation with two workers, run the following commands in individual shells:

```bash
podman-compose --file docker/compose-services.yaml up

uv run --env-file=.env celery -A stackcalc.api worker --loglevel=INFO -n worker1@%h

uv run --env-file=.env celery -A stackcalc.api worker --loglevel=INFO -n worker1@%h

uv run --env-file=.env main.py
```

**access**

- [flower dashboard](http://localhost:5555/) - `http://localhost:5555/`
- [API docs & sandbox](http://localhost:8000/api/v1/docs) - `http://localhost:8000/api/v1/docs`
- [redis database](localhost:6379) - `localhost:6379`