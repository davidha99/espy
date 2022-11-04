FROM ubuntu

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get -y install python3-pip
RUN pip install --upgrade pip
# COPY requirements.txt /tmp/
# RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src

COPY src/ /src/
# RUN pip install -e /src

WORKDIR /src
# CMD python3 compiler.py