FROM python:3.11-slim

RUN apt-get update && \
    apt-get -y upgrade

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY /init_catalogs /app/init_catalogs

CMD ["python", "-m", "init_catalogs"]
