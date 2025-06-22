FROM node:22-bookworm

WORKDIR /ctf

COPY ./package.json .
COPY ./package-lock.json .
COPY ./main.js .
COPY ./flag.txt .
COPY ./boxed.db .
COPY ./views ./views

RUN npm ci

EXPOSE 3000

ENTRYPOINT ["node", "main.js"]
