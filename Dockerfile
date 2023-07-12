FROM python:3.10.6-alpine3.16
LABEL maintainer = "anibal99"

ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi &&\
    rm -rf /tmp

RUN mkdir /app
WORKDIR /app

ADD ./app /app

ARG DEV=false
