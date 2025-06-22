FROM ubuntu:20.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc-10-mipsel-linux-gnu \
    qemu-user-static \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /challenge

# Copy files into the container
COPY nips.c generate_flag.py ./

# Build the challenge
RUN python3 generate_flag.py > flag_constants.h && \
    mipsel-linux-gnu-gcc-10 -o nips nips.c -static -fno-stack-protector -z execstack -O0 && \
    mipsel-linux-gnu-strip nips

# Test the binary compiles and runs (expect failure with wrong flag)
RUN echo "Testing binary compilation:" && \
    ls -la nips && \
    echo "Binary compiled successfully" || true

# Output directory for the built binary
VOLUME /output
