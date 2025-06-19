FROM ubuntu:24.04 AS build

RUN apt-get update && apt-get install -y wget gcc tar make bzip2 nasm && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c "https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c" \
    && gcc -o ynetd ynetd.c && rm ynetd.c && chmod +x ./ynetd

WORKDIR /app

COPY main.asm .
COPY Makefile .

RUN make 

