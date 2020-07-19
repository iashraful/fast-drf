FROM python:3.8.1-alpine
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

WORKDIR /app/server
COPY requirements.txt /app/server
RUN pip3 install -r requirements.txt
#CMD [ "python /app/server/manage.py migrate" ]
