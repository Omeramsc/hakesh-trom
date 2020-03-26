FROM ubuntu:18.04

RUN apt-get -y update && \
    apt-get install -y python python-dev python-pip && \
    snap install --classic heroku

WORKDIR /data
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["heroku", "local", "web"]