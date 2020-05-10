FROM python:3.8.2-slim-buster

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc netcat gettext-base gettext libgettextpo-dev

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

# Django raises a permissions exception when trying to write migrations to flatpages, necessary for django modeltranslation
# Using MIGRATION_MODULES (i.e. using user-writable app directory for flatpage migrations) in settings fails to write tables to db
# Subclassing flatpage model throws an error with modeltranslation
# Other option would be virtualenv inside container. Seems like overkill
# Unecessary in deployment at any rate as db is not flushed after build
RUN chown -R $USERNAME:$USERNAME /usr/local/lib/python3.8/site-packages/
RUN chown -R $USERNAME:$USERNAME /app
USER $USERNAME

ENTRYPOINT ["/app/entrypoint.sh"]
