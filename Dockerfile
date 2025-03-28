FROM python:3.13-alpine3.21

# Logs everything directly to output, do not buffer anything
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src

USER root