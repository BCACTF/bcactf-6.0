FROM ubuntu@sha256:86ac87f73641c920fb42cc9612d4fb57b5626b56ea2a19b894d0673fd5b4f2e9 AS build

RUN apt-get update && apt-get install -y wget gcc && rm -rf /var/lib/apt/lists/* \
    && wget -O ynetd.c "https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c" \
    && gcc -o ynetd ynetd.c && rm ynetd.c && chmod +x ./ynetd

FROM denoland/deno:2.3.6
WORKDIR /app
COPY src .
COPY --from=build ynetd .
EXPOSE 1337
RUN deno install

CMD ./ynetd -p 9990 "deno run -R main.ts"