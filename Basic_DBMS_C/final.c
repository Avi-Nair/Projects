//including necessary header files to run the program

#include<stdio.h>
#include<string.h>
#include<sys/stat.h>
#include<ctype.h>
#include<stdlib.h>
#include<dirent.h>

enum login {No_Match, Match};
typedef enum command {create, addrow, display, delete, logout, Exit, list} COMMAND;

//struct to store enum values and their correspond string values, to convert text command recieved as input to enum
const static struct {
    COMMAND cmd;
    const char *str;
} conversion [] = {
	{create, "create"},
	{addrow, "addrow"},
	{display, "display"},
	{delete, "delete"},
	{logout, "logout\n"},
	{Exit, "exit\n"},
	{list, "list\n"}
};

// function to convert string fragment from command to enum
COMMAND str2enum (const char *str)
{
//j, variable to loop
	int j;
	for (j = 0;  j < sizeof (conversion) / sizeof (conversion[0]);  ++j)
	{
		//comparing string to strings stored in struct
		if (!strcmp (str, conversion[j].str))
		{
			//returning respective enum value
			return conversion[j].cmd;
		}
	}
}

//declaring function prototypes

int authenticate_user();
int create_user();
int create_table(char *cmd_part);
int add_row(char *cmd_part);
int display_table(char *cmd_part);
int delete_table(char *cmd_part);
int delete_row(char *cmd_part);
int list_tables();
void encrypt(char *values);
void decrypt(char *values);

//declaring key and current user global variables to be freely used in any function
char key[30], current_user[30];


//main program

int main()
{
	//enum to print login result
	
	enum login auth;
	
	//restart label, to continue after one user logs out
	restart:
	
	//calling function for user to log in
	auth = authenticate_user();
	
	//printing result of authentication/login process
	switch (auth)
	{
		case 0:
		printf("Invalid credentials\n");
		goto restart;
		break;
		case 1:
		printf("Login successful\n");
		break;
	}
	
	//going to directory named after current user to access tables more easily
	chdir(current_user);
	
	//declaring variable to store command entered
	char cmd_str[100], *cmd_part;
	
	//clearing string of garbage values
	strcpy(cmd_str, "\0");
	
	//declaring enum to perform functions based on command recieved
	COMMAND cmd;
	
	//next command label to continue code after executing one command
	nextcmd:
	
	//recieving command as string
	printf("USER - %s/  ", current_user);
	strcpy(cmd_str, "\0");
	fgets(cmd_str, 100, stdin);
	
	//splitting command and getting enum value to use switch case
	cmd_part = strtok(cmd_str, " ");
	cmd = str2enum(cmd_part);
	int res = 0;
	
	//switch case to perform function based on recieved command
	switch (cmd)
	{
		//creating a tavle
		case 0:
		
		cmd_part = strtok(NULL, " ");
		res = create_table(cmd_part);

		//switch case to display the appropriate result
		switch (res)
		{
			case 0:
			printf("USER - %s/  Table created successfully\n", current_user);
			break;
			case 1:
			printf("USER - %s/  Table already exists\n", current_user);
			break;
			case 2:
			printf("USER - %s/  Invalid command\n", current_user);
			break;
		}

		//going back to the nexcmd label to implement further commands
		goto nextcmd;
		break;
		
		//adding a row
		case 1:
		
		cmd_part = strtok(NULL, " ");
		int add_success = add_row(cmd_part);

		//switch case to display the appropriate result
		switch (add_success)
		{
			case 0:
			printf("USER - %s/  Added row\n", current_user);
			break;
			
			case 1:
			printf("USER - %s/  Table does not exist\n", current_user);
			break;
			
			case 2:
			printf("USER - %s/  Invalid command\n", current_user);
			break;
		}

		//going back to the nexcmd label to implement further commands
		goto nextcmd;
		break;
		
		//displaying the table
		case 2:
		
		cmd_part = strtok(NULL, " ");
		int display_check = display_table(cmd_part);//calling the function to diplay the table

		//switch case to display the appropriate result
		switch (display_check)
		{
			case 0:
			printf("\nUSER - %s/  Contents displayed\n", current_user);
			break;
			
			case 1:
			printf("USER - %s/  Table does not exist\n", current_user);
			break;
			
			case 2:
			printf("USER - %s/  Invalid command\n", current_user);
			break;
		}

		//going back to the nexcmd label to implement further commands
		goto nextcmd;
		break;
		
		//deleting a table or row
		case 3:
		
		int deletion_success;
		cmd_part = strtok(NULL, " ");

		//deleting a table
		if (strcmp(cmd_part, "table")==0)
		{
			cmd_part = strtok(NULL, " \n");
			if (cmd_part==NULL)
			{
				deletion_success = 3;
			}
			else
			{
				deletion_success = delete_table(cmd_part);//calling the function to delete the table
			}
		}

		//deleting a row
		else if (strcmp(cmd_part, "row")==0)
		{
			cmd_part = strtok(NULL, " \n");
			if (cmd_part==NULL)
			{
				deletion_success = 3;
			}
			else
			{
				deletion_success = delete_row(cmd_part);//calling the function to delete a row
			}
		}

		//if invalid value to be deleted given
		else
		{
			deletion_success = 3;		
		}
		
		//switch case to display the appropriate result
		switch (deletion_success)
		{
			case 0:
			
			printf("USER - %s/  Deleted successfully\n", current_user);
			break;
			
			case 1:
			
			printf("USER - %s/  Table not found\n", current_user);
			break;
			
			case 2:
			
			printf("USER - %s/  Row not found\n", current_user);
			break;
			
			case 3:
			
			printf("USER - %s/  Invalid command\n", current_user);
			break;
			
			case 4:
			
			printf("USER - %s/  Aborted\n", current_user);
			break;
			
			default:
			
			printf("SEGF");//segmentation fault
			break;
		}

		//going back to the nexcmd label to implement further commands
		goto nextcmd;
		break;
		
		//logging out from the user profile
		case 4:
		printf("USER - %s/  Logout Successful\n", current_user);
		chdir("..");
		chdir("20cys113_Project");

		//going to restart label after logging out
		goto restart;
		break; 
		
		//exting the DBMS
		case 5:
		break;
		
		//Listing all the tables for the user
		case 6:
		printf("USER - %s/  List of existing tables - \n", current_user);
		int no_of_tables = list_tables();
		printf("%d tables successfully listed\n", no_of_tables);

		//going back to the nexcmd label to implement further commands
		goto nextcmd;
		break;
		
		//for all invalid commands
		default:
		printf("Invalid command\n");

		//going back to the nexcmd label to implement further commands
		goto nextcmd;
		break;
	}
}

//function to authenticate user
int authenticate_user()
{
	char line[65],username[30], password[30], *u_name, *p_word;
	
	printf("\nUsername- ");
	scanf("%s", username);
	
	
	FILE *userlist;
	userlist = fopen("userlist.txt", "r"); //userlist file stores the usernames and passwords seperated with ';'

	//handling file not found exception
	if (userlist==NULL)
	{
		printf("Unable to open file");
	}
	
	
	int username_found=0, condition=0;
	
	//reading the username from the file
	while (condition == 0)
	{
		fgets(line, 65, userlist);
		if (!feof(userlist))
		{
			line[strlen(line)-1]='\0';
			u_name = strtok(line, ";");
			p_word = strtok(NULL, ";");
			if (strcmp(u_name, username)==0)
			{
				username_found = 1;
				condition = 1;
			}
		}
		else
		{
			condition = 1;
		}
	}
	
	
	rewind(userlist);
	
	if (username_found==1)
	{
		//asking the user to enter their password
		printf("Password-");
		scanf("\n%s", password);
		condition = 0;
		while (condition == 0)
		{
			fgets(line, 65, userlist);
			if (!feof(userlist))
			{
				line[strlen(line)-1]='\0';
				u_name = strtok(line, ";");
				p_word = strtok(NULL, ";");
				if (strcmp(u_name, username)==0)
				{
					//checking whether the password is correct
					if (strcmp(p_word, password)==0)
					{
						condition = 1;
						strncpy(current_user, username, 30);
						strncpy(key, password, strlen(password));
						return 1;
					}
					else
					{
						condition = 1;
						return 0;
					}
				}
			}
			else
			{
				return 2;
			}
		}
	}
	
	//if user not found
	else
	{
		char choice;
		printf("User not found, create new? y/n");
		scanf("\n%c", &choice);
		if (choice=='y')
		{
			return create_user(username);
		}
		else
		{
			return authenticate_user();
		}
	}
	
	
	fclose(userlist);

}

//function to create a user
int create_user(char username[])
{
	int check=0;

	//checking that the username entered is alphanumeric
	for (int i=0; i<strlen(username) ; i++)
	{
		if (isalnum(username)!=1)
		{
			check+=1;
		}
	}

	if (check>0)
	{
		FILE *userlist;
		userlist = fopen("userlist.txt", "a");
		
		//handling the file not found exception
		if (userlist==NULL)
		{
			printf("Unable to open file");
		}

		//entering the username into the file
		fputs(username, userlist);
		fputc(';', userlist);
		int loopbreak=1;
		char password[30], confirm_pass[30];

		//asking the user to create a password
		do
		{
			printf("Enter password - ");
			scanf("%s", password);
			printf("Confirm Password - ");
			scanf("%s", confirm_pass);
			if (strcmp(password, confirm_pass)==0)
			{
				fputs(password, userlist);//entering the password into the file
				loopbreak=0;
			}
		}while(loopbreak!=0);
		fputc('\n', userlist);
		fclose(userlist);
		mkdir(username, 0777);
		return 0;
	}

	//if invalid username
	else
	{
		printf("Invalid username");
		authenticate_user();
	}
}		

//function to create a table
int create_table(char *cmd_part)
{
	FILE *check_table;
	char table_name[15];
	if (cmd_part!=NULL)
	{
		
		strcpy(table_name, "\0");
		strncat(table_name, cmd_part, strlen(cmd_part));
		strncat(table_name, ".txt", 5);

		check_table = fopen(table_name, "r");
		if (check_table!=NULL)
		return 1;
		
		cmd_part = strtok(NULL, " ");
		if (cmd_part == NULL)
		return 2;
		
		for (int i = 0; i < strlen(cmd_part); i++)
		{
			if (*(cmd_part+i)<48 && *(cmd_part+i)>57)
			return 2;
		}
		int no_of_cols = atoi(cmd_part);
			
		char line[150];
		strncpy(line, cmd_part, strlen(cmd_part));
		strncat(line, ",", 2);
		for (int i = 0; i<no_of_cols ; i++)
		{
			cmd_part= strtok(NULL, " \n ");
			if (cmd_part == NULL)
			{
				return 2;
			}
			strncat(line, cmd_part, strlen(cmd_part));
			strncat(line, ",", 2);
		}
		
		
		FILE *table_fp = fopen(table_name, "w+");
		encrypt(line);
		
		strncat(line, "\n", 2);
		
		fputs(line, table_fp);
		fclose(table_fp);
		return 0;
	}
	return 2;
}

//function to add a row
int add_row(char *cmd_part)
{
	FILE *table_fp;
	char table_name[15];
	if (cmd_part!=NULL)
	{
	
		strcpy(table_name, "\0");
		strncat(table_name, cmd_part, strlen(cmd_part));
		strncat(table_name, ".txt", 5);
			
		table_fp = fopen(table_name, "r+");//opening the table file in read and write mode
		
		if (table_fp==NULL)
		{
			return 1;
		}
		
		char line[150];
		fgets(line, 150, table_fp);
		decrypt(line);
		char col_nos[2];
		
		for (int i = 0; i < strlen(line); i++)
		{
			if (line[i]==',')
			break;
			else
			col_nos[i] = line[i];
		}
		
		//getting the number of columns in the table
		int no_of_cols = atoi(col_nos);
		
		//getting the number of rows in the table
		int row_count = 0;
		while(!feof(table_fp))
		{
			fgets(line, 150, table_fp);
			row_count++;
		}
		
		char rowcount[3];
		sprintf(rowcount, "%d", row_count);
		strcpy(line, "\0");
		strncat(line, rowcount, strlen(rowcount));
		strncat(line, ",", 2);
		
		//seperating the entered row into seperate column values
		for (int i = 0; i<no_of_cols ; i++)
		{
			cmd_part = strtok(NULL, " \n");
			if (cmd_part == NULL)
			{
				return 2;
			}
			strncat(line, cmd_part, strlen(cmd_part));
			strncat(line, ",", 2);
		}
		
		
		encrypt(line);//encrypting the data before entering it into the file
		
		strncat(line, "\n", 2);
		
		fputs(line, table_fp);//writing the row into the table file
		fclose(table_fp);
		return 0;
	}
	return 2;
}

//function to display all rows in a table
int display_table(char *cmd_part)
{
	FILE *table_fp;
	char table_name[15];
	if (cmd_part!=NULL)
	{
		char *table = strtok(cmd_part, "\n");
		strcpy(table_name, "\0");
		strncat(table_name, table, strlen(table));
		strncat(table_name, ".txt", 5);
			
		table_fp = fopen(table_name, "r");//opening the file where the table is stored
		
		if (table_fp==NULL)
		{
			return 1;
		}
		
		char line[150];
		int i=0;
		printf("\n\n");
		fgets(line, 150, table_fp);
		decrypt(line);//decrypting the data before displaying it

		while(line[i]!=',')
		{
			i++;
			printf("0");
		}
		printf("  |  ");
		
		int count = 3;
		while(i<strlen(line))
		{
			
			if (line[i]==',')
			{
				printf("  |  ");
			}
			else
			{
				printf("%c", line[i]);
			}
			i++;
		}
		
		for(int j = 0 ; j<count; j++)
		{
			printf("__");
		}
		printf("\n");

		
		while(!feof(table_fp))
		{
			strcpy(line,"\0");
			fgets(line, 150, table_fp);
			decrypt(line);
			i=0;
			while (i<strlen(line))
			{
				if (line[i]==',')
				{
					printf("  |  ");//seperating the rows
				}
				else
				{
					printf("%c", line[i]);//printing the row data
				}
				i++;
			}
		}
		
		return 0;
	}
	return 2;
}

//function to delete a table
int delete_table(char *cmd_part)
{
	FILE *table_fp;
	char table_name[15];
	printf("%s", cmd_part);
	strcpy(table_name, "\0");
	strncat(table_name, cmd_part, strlen(cmd_part));
	strncat(table_name, ".txt", 5);
		
	table_fp = fopen(table_name, "r");
	if (table_fp==NULL)
	{
		return 1;
	}
	
	//confirming user's choice to delete the table
	char confirm = '0';
	printf("confirm delete table? y/n");
	confirm = getchar();

	if (confirm == 'y' || confirm == 'Y')
	{
		remove(table_name);//deleting the table on confirmation
		return 0;
	}
	else 
	{
		return 4;
	}
}

//function to delete a row
int delete_row(char *cmd_part)
{
	int depression = 0, depressed = 0;
	char *row_num = strtok(NULL, " \n");
	printf("%s\n", row_num);
	for (int i = 0; i < strlen(row_num); i++)
	{
		if (*(row_num+i)<48 || *(row_num+i)>57)
		{
			return 3;
		}
	}
	FILE *table_fp;
	char table_name[15];
	strcpy(table_name, "\0");
	strncat(table_name, cmd_part, strlen(cmd_part));
	strncat(table_name, ".txt", 5);
	printf("%s\n", table_name);
			
	table_fp = fopen(table_name, "r");
	if (table_fp==NULL)
	{
		return 1;
	}
	
	//asking for confirmation before deleting
	char confirm[3];
	printf("confirm delete row? y/n");
	fgets(confirm, 3, stdin);
	
	char line[150], check_row_num[4], a[2];
	int check;

	
	if (confirm[0] == 'y' || confirm[0] == 'Y')
	{
		FILE *tempfile = fopen("temp.txt", "w"); //using a temporary file to copy all data except the row to be deleted
		
		
		fgets(line, 149, table_fp);
		fputs(line, tempfile);
		
		//copying the data to temp file
		while(!feof(table_fp))
		{
			strcpy(check_row_num, "\0");
			strcpy(line, "\0");
			fgets(line, 150, table_fp);
			decrypt(line);
			check = 0;
			while(line[check]!=',')
			{
				a[0] = line[check];
				a[1] = '\0';
				strncat(check_row_num, a, 3);
				check++;
			}
			printf("%s %s", check_row_num, row_num);
			if (strcmp(check_row_num, row_num)!=0)
			{
				fputs(line, tempfile);
				depression++;
			}
		}
		
		fclose(tempfile);
		fclose(table_fp);
		remove(table_name);
		table_fp = fopen(table_name, "w");
		tempfile = fopen("temp.txt", "r");
		
		printf("--\n");
		while(!feof(tempfile))
		{
			strcpy(line, "\0");
			fgets(line, 150, tempfile);
			fputs(line, stdout);
		}
		
		rewind(tempfile);
		
		int lci = 1, comma_check;
		char lc[3];
		strcpy(line, "\0");
		fgets(line, 150, tempfile);
		fputs(line, table_fp);

		//copying the new table from temporary file to the main file
		while(!feof(tempfile) && depressed < depression-1)
		{
			sprintf(lc, "%d", lci);
			strcpy(line, "\0");
			fgets(line, 150, tempfile);
			comma_check = 0;
			while(line[comma_check]!=',')
			{
				if (lc[comma_check]!='\0')
				{
					line[comma_check] = lc[comma_check];
				}
				else 
				{
					line[comma_check] = '\0';
				}
				comma_check++;
			}
			encrypt(line);
			fputs(line, table_fp);
			lci++;
			depressed++;
		}	
		
		
		fclose(tempfile);
		fclose(table_fp);
		remove("temp.txt");//deleting temporary file after the row has been deleted
		
		return 0;
	}
	else 
	{
		return 4;
	}
}

//function for displaying all tables under a user
int list_tables()
{	
	int count = 0;
	struct dirent *d;
	
	DIR *dr = opendir(".");
	while ((d= readdir(dr)) != NULL)
	{
		if ((strcmp(d->d_name, ".")!=0) && (strcmp(d->d_name, "..")!=0))
		{
			printf("%d . %s \n", count+1, d->d_name);
			count++;
		}	
	}
	closedir(dr);
	
	return count;
}

//function to encrypt data
void encrypt(char *values)
{
	for (int i=0; i<strlen(values); i++)
	{
		if (i>=strlen(key))
		{
			*(values+i) += key[(i%strlen(key))];
		}
		else
		{
		*(values+i) += key[i];
		}
	}
}

//function for decrypting the 
void decrypt(char *values)
{
	for (int i=0; i<strlen(values)-1; i++)
	{
		if (i>=strlen(key))
		{
			*(values+i) -= key[(i%strlen(key))];
		}
		else
		{
			*(values+i) -= key[i];
		}
	}
}
