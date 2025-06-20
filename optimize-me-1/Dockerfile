FROM ubuntu:24.04 AS build

RUN apt-get update && apt-get install -y wget gcc tar make bzip2 nasm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY slow_flag.c .
COPY Makefile .

RUN make 
