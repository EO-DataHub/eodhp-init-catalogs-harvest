FROM python:3.11-slim

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get -y upgrade

WORKDIR /app

COPY data /app/data

COPY requirements.txt /app

RUN --mount=type=cache,target=/root/.cache/pip python -m pip install -r requirements.txt

COPY /init_catalogs /app/init_catalogs

CMD ["python", "-m", "init_catalogs"]
