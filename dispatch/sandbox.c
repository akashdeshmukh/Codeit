#include<stdio.h>
#include<sys/resource.h>
#include<sys/time.h>
#include<unistd.h>
#include<stdlib.h>
#include<signal.h>
#include<sys/types.h>
#include<string.h>
#include<error.h>

int main(int argc,char *argv[])
{
	pid_t cpid;
	struct rlimit rl;
	int status,ptype;
	size_t jlen;
	ptype = (atoi(argv[2])); //converting 2nd argument to integer which determines language
	printf("\n Ptype = %d \n",ptype);
	//ptype = 1 ;
	char pname[40]=""; //command to execute via system()
	char post[40]="";
	char compile[40]="";
	//char post[] = " 2> error";
	//char compile[]="rm error ; gcc -o file ";
	 // for java program name
	//strcat(compile,argv[1]);
	//strcat(compile,post);

	if(ptype == 1 )  //for c program
	{
		strcpy(post," 2> error");
		strcpy(compile,"rm error ; gcc -o file ");
		strcat(compile,argv[1]);
		strcat(compile,post);
		strcpy(pname,"./file < input > output ");
	}

	if(ptype == 2 )  //for java program
	{
		strcpy(post," 2> error");
		strcpy(compile,"rm error ; javac ");
		strcat(compile,argv[1]);
		strcat(compile,post);
		jlen = strlen(argv[1]);
		strcpy(pname,"java ");
		strncat(pname,argv[1],jlen-5);
		strcat(pname," < input > output");
	}

	if(ptype == 3 )  //for ruby program
	{
		strcpy(pname,"ruby ");
		strcat(pname,argv[1]);
		strcat(pname," < input > output");
	}

	if(ptype == 4 )	 //for python
	{
		strcpy(pname,"python ");
		strcat(pname,argv[1]);
		strcat(pname," < input > output");
	}

	if(ptype == 5 ) //for c++
	{
		strcpy(post," 2> error");
		strcpy(compile,"rm error ; g++ -o file ");
		strcat(compile,argv[1]);
		strcat(compile,post);
		strcpy(pname,"file < input > output ");

	}
//strcat(path,argv[1]);
//char *arg[]={path,NULL};

//--------------------------------------------------------
//	Compiling Program

//--------------------------------------------------------
cpid = fork();
	if(cpid < 0)
	{
	printf("Forking Failed \n");
	}
	else if(cpid == 0)
	{

		if( ptype == 1 || ptype == 2 || ptype == 5 )
		{
		//printf("\n Compile = %s ",compile);
		//printf("\nI am getting error here ");
		status = system(compile);
		//printf("\nI am getting error here toooooo");
		}
		else
		status = 0 ;
       		//  printf("Compile status : %d \n",status);
       		if(status==0)
       		{
       			rl.rlim_cur = 5;
	       		rl.rlim_max = 10;
       			setrlimit (RLIMIT_CPU, &rl);   //CPU Time Limit
       			rl.rlim_cur = 20000000000;
			    rl.rlim_max = 20000010000;
			    setrlimit (RLIMIT_AS,&rl);   // Size limit
       			if(system(pname) == -1 )
       				printf("execl failed");
       			//----------------------------This part will run only when execution get fail

       			//----------------------------
       				//fprintf(stderr,"execl failed\n");
       		}
       		else
       		{
       			printf("\n Compilation failed ");
       		}
	}
	else
	{
		//printf("In Parent \n");
		//printf("Name of Program : [ %d ] \n",cpid);
		//printf("\npid %d",cpid);
		wait(NULL);	//wait for forked process to finish
		printf("\n Exiting ");
		//exit(0);
	}
return 0;
}
