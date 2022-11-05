FROM ubuntu

RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip && pip install --upgrade pip \
    && apt install vim -y

RUN mkdir -p /src
WORKDIR /src
COPY ./src .
