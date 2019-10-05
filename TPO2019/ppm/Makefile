NAME=tpo
OBJECTS=main.o ppmp3.o tpo.o

CFLAGS="-g"
ASFLAGS="-g"


all: $(OBJECTS) link

link:
	$(CC) $(OBJECTS) -o $(NAME)

.c.o:
	$(CC) -c $(CFLAGS) $< -o $@

.s.o:
	$(CC) -c $(ASFLAGS) $< -o $@

clean:
	rm $(OBJECTS) $(NAME)
