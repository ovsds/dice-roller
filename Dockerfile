ARG BASE_BUILDER_IMAGE=python:3.12.1
ARG BASE_RUNTIME_IMAGE=python:3.12.1-slim

FROM ${BASE_BUILDER_IMAGE} AS builder

RUN mkdir --parents /opt/app
WORKDIR /opt/app

COPY .poetry-version /opt/app/.poetry-version
RUN python -m pip install "poetry==$(cat /opt/app/.poetry-version)"

COPY .python-version /opt/app/.python-version
COPY pyproject.toml /opt/app/pyproject.toml
COPY poetry.lock /opt/app/poetry.lock
COPY poetry.toml /opt/app/poetry.toml

RUN poetry install --all-extras

FROM ${BASE_RUNTIME_IMAGE} AS runtime

RUN mkdir --parents /opt/app
WORKDIR /opt/app

COPY --from=builder /opt/app/.venv /opt/app/.venv
COPY dice_roller /opt/app/dice_roller

ENTRYPOINT [".venv/bin/python", "-m", "dice_roller.bin.main"]

FROM builder AS builder_dev

RUN poetry install --with dev --all-extras

FROM runtime AS runtime_dev

COPY --from=builder_dev /opt/app/.venv /opt/app/.venv
COPY pyproject.toml /opt/app/pyproject.toml

FROM runtime_dev AS tests

COPY tests /opt/app/tests
ENV TESTS_ENVIRONMENT=CONTAINER

ENTRYPOINT [".venv/bin/python", "-m", "pytest", "tests"]
