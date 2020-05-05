FROM python:3.8.2-slim-buster

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc netcat

WORKDIR /app
COPY ./requirements /app/requirements
RUN pip install -r /app/requirements/dev.txt

RUN apt-get autoremove -y gcc

ENV USERNAME=app
ENV UID=1000
ENV GID=1000
RUN addgroup --system --gid $GID $USERNAME && adduser --disabled-password --gecos '' --system --uid $UID $USERNAME

WORKDIR /app
COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh

RUN chown -R $USERNAME:$USERNAME /usr/local/lib/python3.8/site-packages/
RUN chown -R $USERNAME:$USERNAME /app
USER $USERNAME

ENTRYPOINT ["/app/entrypoint.sh"]
