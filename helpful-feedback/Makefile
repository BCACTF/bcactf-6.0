CC=g++
CFLAGS=-O0 -g -Wall -Wextra
BINARY=help

all: $(BINARY)

$(BINARY): challenge.cpp
	$(CC) $(CFLAGS) -o $(BINARY) slow_flag.c -lm

debug: challenge.cpp
	$(CC) -O0 -g3 -Wall -Wextra -o $(BINARY)_debug slow_flag.c -lm

optimized: challenge.cpp
	$(CC) -O3 -DNDEBUG -o $(BINARY)_fast slow_flag.c -lm

clean:
	rm -f $(BINARY) $(BINARY)_debug $(BINARY)_fast

.PHONY: all debug optimized clean