FROM python:3.12.4-slim

WORKDIR /usr/src/app/backend
ENV FLASK_APP=api
ENV FLASK_ENV=development

COPY /requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt