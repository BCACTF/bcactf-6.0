FROM ubuntu:20.04 AS build

RUN apt-get update -y && apt-get install -y gcc wget && rm -rf /var/lib/apt/lists/* \
    && wget -Oynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
    && gcc -o ynetd ynetd.c

FROM python:3.12-slim-bookworm

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf
COPY expletive.py .
COPY flag.txt .
COPY --from=build ynetd ynetd
RUN chmod +x ynetd && chown -R root:root /home/ctf 

USER ctf
EXPOSE 9990
CMD ["./ynetd", "-p", "9990", "python3 expletive.py"]