CC = gcc
CFLAGS = -Wall -g

all: mallocTest

mallocTest: duMalloc.o mallocTest.o
	$(CC) $(CFLAGS) -o mallocTest duMalloc.o mallocTest.o

duMalloc.o: duMalloc.c
	$(CC) $(CFLAGS) -c duMalloc.c

mallocTest.o: mallocTest.c
	$(CC) $(CFLAGS) -c mallocTest.c

clean:
	rm -f *.o mallocTest
