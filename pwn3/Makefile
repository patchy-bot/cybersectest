CC = gcc

all: clean vuln

vuln:
	$(CC) -fno-stack-protector -no-pie -m32 vuln.c -o vuln
clean:
	rm -f vuln
