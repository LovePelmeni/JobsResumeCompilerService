FROM --platform=linux/amd64 python:3.8.13-buster
MAINTAINER Kirill Klimushin, email: kirklimushin@gmail.com

RUN mkdir /project/dir/
WORKDIR /project/dir/

ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
COPY . .
RUN pip install psycopg2-binary --no-input --no-cache-dir
RUN cd ./JobsResumeCompiler/API/project/
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["sh", "./entrypoint.sh"]


