#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

char **files;
int count;
int maxsize;

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

int getint() {
    char buffer[32];
    get_inp(buffer, 32);
    return atoi(buffer);
}

void initialise()
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
	chdir("./data");
  files=(char**)malloc(100*sizeof(char*));
  maxsize=100;
  count=0;
}

void listdir()
{
    DIR *d;
    struct dirent *dir;
    d = opendir(".");
    if (d)
    {
        while ((dir = readdir(d)) != NULL)
        {
            if(count>=maxsize)
            {
              files=(char**)realloc(files,maxsize+(100*sizeof(char*)));
              maxsize+=100;
            }
            char* temp=(char*)malloc(strlen(dir->d_name)*sizeof(char)+1);
            strncpy(temp, dir->d_name, strlen(dir->d_name));
            files[count]=temp;
            count++;
        }
        closedir(d);
    }
}

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

int check_existence(char* username, bool* exists)
{
  int flag=0;
  for(int i=0;i<count;i++)
  {
    if(!strcmp(username, files[i]))
    {
      exists[i]=true;
      flag=1;
    }
    else
    {
      exists[i]=false;
    }
  }
  return flag;
}

void save(char* user)
{
  listdir();

  char* temp=(char*)malloc(50*sizeof(char));
  bool* exist=(bool*)malloc(count*sizeof(bool));
  int size=0;


  if(!check_existence(user,exist))
  {
    FILE *fp;
    fp=fopen(user, "w");
    printf("Enter size (<50): ");
    size=getint();
    if(size>=50)
    {
      puts("Sorry, Your data is too big!");
      exit(0);
    }
    printf("Enter input: ");
    get_inp(temp, size);
    fprintf(fp, "%s", temp);
    fclose(fp);
    puts("Input saved successfully.");
  }
  else
  {
    puts("save: Permission denied. You can only view :- ");
  }

  for(int i=0;i<count;i++)
  {
    if(exist[i])
    {
      readfile(files[i]);
    }
  }

  return;
}



void view(char* user)
{
  int len;
  int flag=0;
  listdir();
  for(int i=0;i<count;i++)
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

void menu()
{
  puts("=======Menu======");
  puts("1. Save message");
  puts("2. View message");
  printf("Your choice: ");
}

int main(int argc, char const *argv[]) {
  char user[100];
  int opt;

  initialise();

  printf("Enter username: "); 
  get_inp(user, 100);

  menu();
  opt=getint();
  switch(opt)
  {
    case 1: save(user);
            break;
    case 2: view(user);
            break;
    default: puts("Invalid Choice");
  }

  return 0;
}

