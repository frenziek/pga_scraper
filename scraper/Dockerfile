FROM python:slim-bookworm

WORKDIR /scraper

ENV FLASK_RUN_HOST=127.0.0.1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /scraper
