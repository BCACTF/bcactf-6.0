CC=gcc
CFLAGS=-O0 -g -Wall -Wextra
BINARY=slow_flag

all: $(BINARY)

$(BINARY): slow_flag.c
	$(CC) $(CFLAGS) -o $(BINARY) slow_flag.c -lm

debug: slow_flag.c
	$(CC) -O0 -g3 -Wall -Wextra -o $(BINARY)_debug slow_flag.c -lm

optimized: slow_flag.c
	$(CC) -O3 -DNDEBUG -o $(BINARY)_fast slow_flag.c -lm

clean:
	rm -f $(BINARY) $(BINARY)_debug $(BINARY)_fast

.PHONY: all debug optimized clean
