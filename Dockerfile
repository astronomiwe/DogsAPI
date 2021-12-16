FROM python:3.9.5-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend_v2


RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc libssl-dev -y

COPY . /backend_v2/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

