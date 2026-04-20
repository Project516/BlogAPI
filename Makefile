CC = gcc

TARGET = BlogAPI

SRC = src/main.c src/mongoose.c

CFLAGS = -Wall -Iinclude

all:
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)