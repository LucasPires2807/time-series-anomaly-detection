FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app
ADD . /app

RUN uv sync --frozen --no-install-project

RUN uv sync --frozen

CMD ["uv", "run", "gunicorn", "-c", "gunicorn.conf.py"]