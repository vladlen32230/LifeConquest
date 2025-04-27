FROM python:3.10.15-alpine3.20

WORKDIR /lifeconquest
COPY . .
COPY ./docker/server/.letsencrypt /etc/letsencrypt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
