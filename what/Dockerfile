FROM php:8.2-cli-bookworm

WORKDIR /app

COPY what.php .
COPY flag.txt .

EXPOSE 3000

ENTRYPOINT ["php", "-S", "0.0.0.0:3000", "what.php"]
