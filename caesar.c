#include <cs50.h>
#include <stdio.h>
#include <string.h>
int main(int argc, string argv[])
{
    if(argc<1 || argc>2 || argv[1]==0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {
        printf("succes\n");
    }
    int k = atoi(argv[1]);
    string s = get_string("plaintext : ");
    printf("ciphertext : ");
    for( int i=0; i<strlen(s);i++)
    {
   
        int c =(int) s[i];
        if(c!=32 && c!=44) 
        {
        c= c +k;
        }
        while(c>=123)
        {
        c= (c % 122)+96;
        }
        char r=(char) c;
        
        printf("%c",c);
    }
    printf("\n");
}
