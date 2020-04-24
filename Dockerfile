FROM python:3.8.0-alpine

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add build-base musl-dev gcc postgresql-dev python3-dev zlib-dev jpeg-dev openssl-dev libffi-dev \
        && pip install --upgrade pip


WORKDIR /app
COPY ./requirements /app/requirements
RUN pip install -r /app/requirements/dev.txt

COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh

ENV UNAME=app
ENV UID=1000
RUN addgroup -S $UNAME && adduser --disabled-password --gecos '' -S $UNAME -g $UNAME --uid $UID
USER $user

ENTRYPOINT ["/app/entrypoint.sh"]
