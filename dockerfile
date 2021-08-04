FROM python:3.6

RUN apt update -y && apt upgrade -y
RUN PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip setuptools
RUN pip install --requirement requirements.txt
