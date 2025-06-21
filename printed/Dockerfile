FROM ubuntu:24.04 AS build

RUN apt-get update && apt-get install -y wget gcc && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c "https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c" \
    && gcc -o ynetd ynetd.c && rm ynetd.c && chmod +x ./ynetd 


FROM ubuntu:24.04

RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

COPY --from=build ynetd .
RUN chmod +x ynetd

COPY printed .
COPY flag.txt .

RUN chown -R root:root /home/ctf 

EXPOSE 8626
CMD ["./ynetd", "-p", "8626", "./printed"]