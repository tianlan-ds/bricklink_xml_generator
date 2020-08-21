FROM python:3.7

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y tzdata vim

RUN pip3 install lxml
RUN pip3 install bs4
