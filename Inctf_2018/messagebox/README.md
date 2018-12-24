### messagebox (Attack and Defense)
---
<p>messagebox is a tcp server which allows us to read and save files in directory named data.</p>
<p>service is  running on port <code>5050</code></p>

<p>Actually, it asks username and read/write the file name with that username.</p>

<pre>
<code>
$ ./message
Enter username: s1r1u5
=======Menu======
1. Save message
2. View message
Your choice: 1
Enter size (<50): 30
Enter input: Hello World
Input saved successfully.
</code>
</pre>
<pre>
<code>
$ ./message
Enter username: s1r1u5
=======Menu======
1. Save message
2. View message
Your choice: 2
Hello World
</code>
</pre>
<p style="font-color:red">Let us find our search for finding the vulnerabilities... </p>
<p> Oh wait! Do we have to reverse engineer the binary :flushed? No, we got the source code there <3</p>


