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

The whole repo is set up such that local usage works out of the box. In particular the compose yaml files and the `.env` file facilitate local testing. Take care **not** to put production values inside the `.env` file.

**running**

The quickest way to get started is by running the following one-liner. This builds the images, starts the necessary services, runs the api and a single worker:

```bash
podman-compose --file docker/compose.yaml up
```

**running (multiple workers)**

The easiest way to run multiple workers is by leveraging the *run*-command of `podman-compose`. Override the default celery worker name to have a unique id of each worker. As follows:

```bash
podman-compose --file docker/compose-services.yaml up

podman-compose --file docker/compose.yaml up --no-deps api

CELERY_WORKER_NAME=worker1@%h \
podman-compose --file docker/compose.yaml run --no-deps worker

CELERY_WORKER_NAME=worker2@%h \
podman-compose --file docker/compose.yaml run --no-deps worker
```

**access**

- [flower dashboard](http://localhost:5555/) - `http://localhost:5555/`
- [API docs & sandbox](http://localhost:8000/api/v1/docs) - `http://localhost:8000/api/v1/docs`
- [redis database](localhost:6379) - `localhost:6379`

## Development

To rebuild all the images after some change:

```bash
podman-compose --file docker/compose.yaml build
```

## Deployment

The instructions given here are targeted towards [koyeb](https://www.koyeb.com/). It should be straightforward to adapt to any cloud provider.

Two services are installed in the service mesh, straight from docker. They are `docker.io/rabbitmq` for the broker and `docker.io/redis` for the backend.

The api is installed as a public web service. One or more workers are installed as private workers in the service mesh. We assume for now that a single worker is installed on a node. Don't forget to set the environment variable `CELERY_WORKER_NAME` to a unique identifier for every worker. Which environment variables (from `.env`) are required for which service is visible in the file `compose-api.yaml`.