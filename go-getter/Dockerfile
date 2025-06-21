FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy source code
COPY main.go .

# Build the binary with some obfuscation flags
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-w -s -extldflags "-static"' -o go-getter main.go

# Final stage - minimal image
FROM scratch

# Copy the binary
COPY --from=builder /app/go-getter /go-getter

# Set the entrypoint
ENTRYPOINT ["/go-getter"]
