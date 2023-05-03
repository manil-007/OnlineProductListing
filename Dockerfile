FROM ubuntu

LABEL MAINTAINER="Ankur Vatsa"
LABEL GitHub="https://github.com/vatsaaa"
LABEL version="1.0"
LABEL description="A Docker container to serve Python API for Online Product Listing Creator"

RUN apt update && apt upgrade -y && apt install nodejs -y && apt install npm -y && npm install pm2 -g

WORKDIR /app
COPY . /app

RUN apt install python3 -y && apt install python3-pip -y && pip3 install --upgrade pip && pip3 install -r requirements.txt

RUN set -ex apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

CMD ["python3", "main.py", "-h"]
