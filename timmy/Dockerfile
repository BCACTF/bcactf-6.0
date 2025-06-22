FROM node:22-bookworm

WORKDIR /ctf/app

COPY ./app .
COPY ./flag.txt ./private

RUN npm ci
RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

ENTRYPOINT ["node", "build"]
