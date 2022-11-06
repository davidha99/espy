FROM i386/ubuntu

RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip && pip3 install --upgrade pip \
    && apt-get install vim -y && pip3 install pudb

RUN mkdir -p /src
WORKDIR /src
COPY ./src .
