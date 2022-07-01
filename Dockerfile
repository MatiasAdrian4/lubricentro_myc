# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /lmyc
COPY django_project /lmyc/
RUN pip install -r requirements.txt