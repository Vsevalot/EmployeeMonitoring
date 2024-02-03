FROM python:3.11-alpine as base

ENV MUSL_LOCPATH=en_US.utf8 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# RUN apk update && apk add gcc g++

WORKDIR /opt/app/
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

FROM base as builder

RUN --mount=type=cache,target=/root/.cache \
    pip3 install poetry --disable-pip-version-check --no-color

COPY poetry.lock pyproject.toml /opt/app/

RUN --mount=type=cache,target=/root/.cache \
    poetry export -f requirements.txt -o requirements.txt


FROM base as app

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,from=builder,source=/opt/app/requirements.txt,target=/opt/app/requirements.txt \
    pip3 install -r requirements.txt

ADD . /opt/app

ENTRYPOINT ["python", "main.py"]

