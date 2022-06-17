FROM ubuntu:18.04
ARG USER=linux_user
RUN adduser -disabled-password --gecos '' $USER

USER linux_user

RUN apt-get update && \ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
apt-get install apt-transport-https ca-certificates curl software-properties-common && \
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
apt-get update && \ apt-get install docker.ce docker-compose -y && usermod -aG docker $USER

RUN docker -v

RUN mkdir ./app/
RUN cd ./app/
RUN nano Dockerfile

FROM python:3.8.13-buster
MAINTAINER Kirill Klimushin, email: kirklimushin@gmail.com

WORKDIR /app/
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install psycopg2-binary --no-input --no-cache-dir
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "./entrypoint.sh"]