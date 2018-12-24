#include<stdio.h>
#include<string.h>
int get_inp(char *buffer, unsigned int len)
{
	int ret=0;
	for(int i=0; i<len; i++)
	{
		read(0,&buffer[i],1);
		if(buffer[i]=='\n')
		{
			buffer[i]='\0';
			break;
		}

		ret++;
	}
	return ret;
}


int main(){
    char user[100];

	char buf[]	 = "hello";
	printf("%s\n", buf);
	get_inp(user, 100);
	int len = 0;
	int s = strncmp(user, buf,len);
	printf("%d\n",s);



}