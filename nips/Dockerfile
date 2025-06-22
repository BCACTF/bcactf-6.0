FROM ubuntu:20.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc-mips-linux-gnu \
    qemu-user \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /challenge

# Copy files into the container
COPY nips.c generate_flag.py ./

# Build the challenge
RUN python3 generate_flag.py > flag_constants.h && \
    mips-linux-gnu-gcc -include flag_constants.h -o nips nips.c -static -fno-stack-protector -z execstack -O0 && \
    mips-linux-gnu-strip nips

# Test the binary
RUN echo "Testing with invalid flag:" && \
    qemu-mips ./nips "WRONG{Th1s_1s_n0t_th3_fl4g}" || true

# Output directory for the built binary
VOLUME /output
