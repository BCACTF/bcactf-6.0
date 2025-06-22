FROM ubuntu:24.04 AS build

RUN apt-get update && apt-get install -y wget gcc tar make bzip2 build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY challenge.cpp .
COPY Makefile .

RUN make 