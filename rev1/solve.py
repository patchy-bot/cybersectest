#!/usr/bin/env python3

encrypted = open('output.txt', 'r').read()

def main():
    flag = ''
    for i in range(0, len(encrypted), 12):
        current = encrypted[i:i+12]
        c = 100 * int(current[0:4], 2)
        c += 10 * int(current[4:8], 2)
        c += int(current[8:12], 2)
        flag += chr(c)
    print(flag)

if __name__ == '__main__':
    main()
