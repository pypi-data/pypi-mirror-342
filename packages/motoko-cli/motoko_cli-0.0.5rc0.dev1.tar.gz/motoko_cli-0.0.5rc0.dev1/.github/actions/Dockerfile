
FROM python:3.11-slim

RUN apt-get update && apt-get install -y git python3 python3-dev && apt-get clean

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install \
  hatch \
  numpy \
  poetry \
  pytest \
  setuptools \
  wheel

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
