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
<p> Oh wait! Do we have to reverse engineer the binary? :flushed: No, we got the source code there. :relieved: Now our only task is to find the vulnerabilities in the source code <a href="message.c">message.c</a>.</p>

<pre><code>
void readfile(char* filename)
{
  char* ptr;
  char* temp="cat ";
  ptr=(char*)malloc(sizeof(char)*(strlen(temp)+strlen(filename)+1));
  strcpy(ptr, temp);
  strcat(ptr, filename);
  system(ptr);
  free(ptr);
  printf("\n");
}
</pre></code>
<p> Are you able to find any vulnerabilities there????</p>
<p> Yes, there it is <b>cat</b> and <b>system</b> call</p>
<p> To read the file called filename from the local directory it is using cat command. Here filename is nothing but the username which we have given.</p>
<h3>Bug 1</h3>
username = *
exploit : <a href="exp.py">exp.py</a>
<p> what if we give the username as *. It just read all the files in the current directory</p>
<h3>Bug 2</h3>
username = *; sh
exploit : <a href="exp3.py">exp3.py</a>
<pre>
<code>
cat *; sh
</code>
</pre>
<p> Now we can get the shell by ending first command by <b>;</b></p>
<h3>Bug 3</h3>
<pre><code>
void view(char* user)
{
  int len;
  int flag=0;
  listdir();
  for(int i=0; i count ;i++)
  {
    len=strlen(user);
    if(!strncmp(user, files[i], len))
    {
      readfile(files[i]);
      flag=1;
    }
  }
  if(!flag)
    puts("No such user");
}
</code></pre>
<p> Another bug if we give empty username as input then strncmp("",files[i],0) is always 0. </p>
exploit : <a href="exp2.py">exp2.py</a>
