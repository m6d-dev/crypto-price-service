FROM python:3.14-alpine


ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=off \
    PROJECT_DIR="/code"


WORKDIR ${PROJECT_DIR}

RUN --mount=type=cache,target=/root/.apk apk update && apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev \
    postgresql17-client \
    curl

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock $PROJECT_DIR/

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install

COPY . $PROJECT_DIR/

RUN chmod +x ${PROJECT_DIR}/scripts/start_api.sh \
  && mkdir -p ${PROJECT_DIR}/media ${PROJECT_DIR}/static \
  && chmod -R 755 ${PROJECT_DIR}/media ${PROJECT_DIR}/static

EXPOSE 8000

CMD ["./scripts/start_api.sh"]
