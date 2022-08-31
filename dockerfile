# CREATE ALPINE BASE IMAGE
# FROM python:3.9.6-alpine
# RUN apk --update --upgrade --no-cache --virtual .tmp add gcc musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev linux-headers libc-dev
# FROM afzalsaiyed/corecare_base:alpine

# CREATE SLIM-BUSTER BASE IMAGE
#FROM python:3.9.6-slim-buster
#RUN apt-get update && apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info -y


# TESTING BUILD
FROM afzalsaiyed/corecare_base:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /corecare_backend
COPY ./requirements/base.txt .
COPY ./requirements/testing.txt .
RUN pip install -r testing.txt
COPY . .
EXPOSE 8000





