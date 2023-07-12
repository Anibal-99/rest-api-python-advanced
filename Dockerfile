FROM python:3.10.6-alpine3.16
LABEL maintainer = "anibal99"

ENV PYTHONUNBUFFERED 1
EXPOSE 8000

COPY ./requirements.txt /requirements.txt
WORKDIR /app
COPY ./app /app

RUN pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    rm -rf /requirements.txt

# Creating user
RUN adduser -D user
USER user
