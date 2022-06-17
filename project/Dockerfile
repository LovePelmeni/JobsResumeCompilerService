FROM ubuntu:18.04
ARG USER=linux_user
RUN adduser -disabled-password --gecos '' $USER

USER linux_user

RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN apt-get install -y curl python3.7 python3.7-dev python.3.7-distutils

MAINTAINER Kirill Klimushin, email: kirklimushin@gmail.com

WORKDIR /app/
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY ./requirements.txt ./requirements.txt
RUN pip install psycopg2-binary --no-input --no-cache-dir
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "./entrypoint.sh"]