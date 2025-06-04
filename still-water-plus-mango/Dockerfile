FROM --platform=linux/amd64 ubuntu:20.04 AS build

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y wget && apt-get install -y unzip && rm -rf /var/lib/apt/lists/*

RUN wget -O ynetd.c https://raw.githubusercontent.com/johnsonjh/ynetd/master/ynetd.c \
  && gcc -o ynetd ynetd.c


RUN useradd -m -d /home/ctf -u 12345 ctf
WORKDIR /home/ctf

# copy over ynetd
COPY --from=build ynetd ynetd 
RUN chmod +x ynetd

# copy over source and set permissions
COPY swpm.c .
RUN gcc -o swpm swpm.c -fno-stack-protector -no-pie -Wl,-z,lazy

RUN chown -R root:root /home/ctf

# run and expose
USER ctf
EXPOSE 4123
CMD ["./ynetd", "-p", "4123", "./swpm"]

