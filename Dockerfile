
FROM python:3.13.0-slim AS base
ENV \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
RUN adduser --disabled-password usal
ARG VENV_PATH="/project/.venv"

FROM base AS build-deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM build-deps AS uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN uv venv ${VENV_PATH}
ENV VIRTUAL_ENV=${VENV_PATH}

WORKDIR /project
COPY pyproject.toml README.md ./
RUN uv pip install -r pyproject.toml

COPY usal ./usal
RUN uv pip install -e .

FROM base AS runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    gcc \
    build-essential \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

FROM runtime AS runner
ENV PATH="/project/.venv/bin:$PATH"
COPY --from=uv ${VENV_PATH} ${VENV_PATH}
COPY . /project/

WORKDIR /project

USER usal
ENTRYPOINT ["make"]

FROM runner AS staging
CMD ["run"]

FROM runner AS local
CMD ["debug"]
