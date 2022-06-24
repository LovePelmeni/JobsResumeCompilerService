FROM python:3.8.13-buster
MAINTAINER Klimushin Kirill kirklimushin@gmail.com

CMD mkdir /dir/project/
WORKDIR /dir/project/
CMD ls
ENV PYTHONUNBUFFERED=1

RUN echo "Starting building Project Image 🍺.
"Project Is Created By <Kirill Klimushin, Email: 'kirklimushin@gmail.com'."

RUN pip install --upgrade pip
RUN pip freeze > requirements.txt
ADD ./requirements.txt ./requirements.txt

COPY . .

RUN pip install -r requirements.txt
RUN pip uninstall psycopg2-binary

RUN pip install psycopg2-binary --no-cache --no-input && \
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["sh", "./docker-entrypoint.sh"]

