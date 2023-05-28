FROM balenalib/raspberry-pi-python:3.10-buster

LABEL maintainer="gallegoj@uw.edu"

WORKDIR /opt

COPY . evora-wheel

RUN apt-get -y update
RUN apt-get -y install build-essential

RUN pip3 install -U pip setuptools wheel
RUN cd evora-wheel && pip3 install .

RUN curl -fsSL https://www.phidgets.com/downloads/setup_linux | bash - &&\
RUN apt-get install -y libphidget22

# Connect repo to package
LABEL org.opencontainers.image.source https://github.com/uwmro/evora-wheel

ENTRYPOINT evora-wheel start --debug
