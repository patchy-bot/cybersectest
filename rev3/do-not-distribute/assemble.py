#!/usr/bin/env python3

program = open('checker.txt', 'r').read()
output = open('checker', 'wb')

for i in program.split('\n'):
    for data in i.split('  ')[1:3]:
        for byte in data.split(' '):
            if len(byte) == 2:
                output.write(bytes.fromhex(byte))

