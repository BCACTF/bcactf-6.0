FROM --platform=linux/amd64 ubuntu:20.04 AS build

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y wget && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

RUN wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
  && gcc -o ynetd ynetd.c


FROM --platform=linux/amd64 python:3.12-slim-bookworm AS deployer

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

# copy over ynetd
COPY --from=build ynetd ynetd 
RUN chmod +x ynetd

# copy over source and set permissions
COPY flag.txt .

COPY server.py .

RUN chown -R root:root /home/ctf

# run and expose
USER ctf
EXPOSE 7330
CMD ["./ynetd", "-p", "7330", "python3 server.py 2>&1"]
