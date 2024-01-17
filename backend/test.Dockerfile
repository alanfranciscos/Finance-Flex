FROM python:3.11-slim-bookworm

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONPATH=/api


WORKDIR /api

# Install dependencies
COPY requirements.txt app/
COPY requirements-test.txt app/
RUN pip install -r app/requirements.txt
RUN pip install -r app/requirements-test.txt
# copy project
COPY app ./app
COPY infra ./infra
COPY tests ./tests

COPY .coveragerc /app/.coveragerc

ENV TZ="UTC"