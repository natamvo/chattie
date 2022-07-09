FROM python:3.10-slim-bullseye

RUN apt-get update -y 
# && pip install tornado
# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN pip install poetry

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

ENTRYPOINT ["sh", "docker-entrypoint.sh"]