FROM nginx:1.27-bookworm

WORKDIR /build

COPY ./build .
COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000
