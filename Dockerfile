FROM python:3.8.1-alpine
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev libffi-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

WORKDIR /app/server
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi
