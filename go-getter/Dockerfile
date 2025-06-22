FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY main.go .

# Build with optimizations and strip symbols
RUN CGO_ENABLED=0 GOOS=linux go build \
    -a -ldflags '-w -s -extldflags "-static"' \
    -o go-getter main.go

FROM scratch
COPY --from=builder /app/go-getter /go-getter
ENTRYPOINT ["/go-getter"]
