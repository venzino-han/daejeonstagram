# /docker-server/server_dev/Dockerfile
FROM python:3.7.3

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /docker-server
ADD . /docker-server

WORKDIR /docker-server

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
