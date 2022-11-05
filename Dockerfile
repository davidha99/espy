# Define working directory.
# RUN mkdir -p /espy/src
# COPY /src/* /espy/src/
# ENTRYPOINT [ "python3", "/espy/src/compiler.py" ]



FROM ubuntu

RUN apt-get update -y && apt-get install -y \
    python3 \
    python3-pip && pip install --upgrade pip

# RUN apt-get update -y
# RUN apt-get install -y python3
# RUN apt-get -y install python3-pip
# RUN pip install --upgrade pip
# # COPY requirements.txt /tmp/
# # RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /src
WORKDIR /src
COPY ./src .

# CMD "bash"

# # RUN pip install -e /src

# ENTRYPOINT [ "python3", "compiler.py" ]