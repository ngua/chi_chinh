FROM python:3.8.2-slim-buster

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc netcat

WORKDIR /app
COPY ./requirements /app/requirements
RUN pip install -r /app/requirements/dev.txt

RUN apt-get autoremove -y gcc

ENV UNAME=app
ENV UID=1000
ENV GID=1000
RUN addgroup --system --gid $GID $UNAME && adduser --disabled-password --gecos '' --system --uid $UID $UNAME

WORKDIR /app
COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh

RUN chown $UNAME:$UNAME /app
USER $UNAME

ENTRYPOINT ["/app/entrypoint.sh"]
