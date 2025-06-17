FROM ubuntu:24.04 AS build

RUN apt-get update && apt-get install -y gcc

WORKDIR /app

COPY shallowseek.c .

RUN  gcc shallowseek.c -o shallowseek && ./shallowseek