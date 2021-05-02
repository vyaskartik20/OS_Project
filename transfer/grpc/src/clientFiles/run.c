#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

#define maxCap 200
#define SPACE ' '
#define EPSILON '?'
#define NULLSPACE '\0'
#define COLON ':'
#define PIPE '|'

int count_R[maxCap], check[maxCap], mapping[maxCap], rulesNT[maxCap];
char L[maxCap], R[maxCap][maxCap][maxCap], rules[maxCap][maxCap][maxCap][maxCap], NT[maxCap][maxCap], T[maxCap][maxCap];

char symbolStart;

int TNum = 0, NTNum = 0, num_rules = 0;


int currIndex = 0;
char rule[maxCap];
char rulesConverted[maxCap];
int rulesConvertedLength = 0;


char* hashCharToString(char c)
{
	return (c>='a')?(T[c-'a']):(NT[c-'A']);
}

void printS(char *s)
{
    int l = strlen(s);
    for(int i=0;i<l ;i++)
    {
        printf("%s ", hashCharToString(s[i]));
    }
}

int handle_check(char symbol)
{
    int l = count_R[symbol];
    for(int i=0;i<l;i++)
    {
        int inc = 0;
        int check=1;
        int leng = strlen(R[symbol][i]);
        for(int j=0;j< leng && check;j++)
        {
            if(isupper(R[symbol][i][j]))
            {
                printf("\n[Called for %s]\n", hashCharToString(R[symbol][i][j]));
                printf("%s -> ", hashCharToString(symbol));
                printS(R[symbol][i]);
                check  = handle_check(R[symbol][i][j]);
            }
            else if(R[symbol][i][j] == EPSILON)
            {
                printf("%s -> ?\n", hashCharToString(symbol));
                break;
            }
            else if(currIndex < rulesConvertedLength && R[symbol][i][j] == rulesConverted[currIndex])
            {
                inc++;
                currIndex++;
                printf("%s matched in %s -> ", hashCharToString(rulesConverted[currIndex-1]), hashCharToString(symbol));
                printS(R[symbol][i]);
                printf("\n");
            }
            else
            {
                if(currIndex < rulesConvertedLength && R[symbol][i][j] != rulesConverted[currIndex])
                {
                    printf("%s not matched with %s\n", hashCharToString(R[symbol][i][j]), hashCharToString(rulesConverted[currIndex]));
                }
                currIndex-=inc;
                check=0;
            }
        }
        if(check) 
        {
            return 1;
        }
    }
    return 0;
}


int presentStringCheck(char arr[][maxCap], int siz, char *s)
{
	for(int i=0;i<siz;i++)
    {
		if(strcmp(arr[i], s) == 0) 
        {
            return 0;
        }
    }
	return 1;
}

int NTCheck(char *s)
{
    for(int i=0;i<NTNum;i++)
    {
        if(strcmp(s, NT[i]) == 0) 
        {
            return 0;
        }
    }
    return 1;
}

char hashStrToChar(char *s)
{
    for(int i=0;i<TNum;i++)
    {
        if(strcmp(s, T[i]) == 0) 
        {
            return (char)('a'+i);
        }
    }
    for(int i=0;i<NTNum;i++)
    {
        if(strcmp(s, NT[i]) == 0) 
        {
            return (char)('A'+i);
        }
    }
}



int main()
{
    //initialisation
	int cnt=0;
    int flagRules;
	memset(mapping, -1, sizeof(mapping));

	
    //input
    scanf("%d", &flagRules);
    scanf("\n");
    int cur=0;
    while(cur < flagRules)
    {
        int cnt=0;
        scanf("%[^\n]%*c", rule);
        if(cur < (flagRules-1))
        {
            scanf("\n");
        }
        int check_check=1;
        int len = strlen(rule);
        int idx=0;
        char *temp = (char *)malloc(maxCap * sizeof(char));
        
        for(int i=0;i<len;i+=1)
        {
            char ch = rule[i];
            if(ch == COLON)
            {
                continue;
            }
            else if(ch == PIPE)
            {
                rulesNT[NTNum]++;
                idx=0;
            }
            else if(ch == SPACE)
            {
                if(cnt > 0)
                {
                    temp[cnt]=NULLSPACE;
                    if(check_check)
                    {
                        strcpy(NT[NTNum], temp);
                        check_check=0;
                    }
                    else
                    {
                    	strcpy(rules[NTNum][rulesNT[NTNum]][idx++], temp);
                    }
                }
                cnt=0;
            }
            else if(iscntrl(ch) == 0)
            {
                temp[cnt++]=ch;
            }
        }
        if(cnt > 0)
        {
            temp[cnt]=NULLSPACE;
            strcpy(rules[NTNum][rulesNT[NTNum]][idx++], temp);
        }
        rulesNT[NTNum]++;
        cur++;
        NTNum++;
    }
    for(int i=0;i<NTNum;i++)
    {
        for(int j=0;j<rulesNT[i];j++)
        {
            for(int k = 0 ; strlen(rules[i][j][k]) > 0 ; k++)
            {
            	if(NTCheck(rules[i][j][k]) && rules[i][j][k][0]!=EPSILON && presentStringCheck(T, TNum, rules[i][j][k]))
                {
                    strcpy(T[TNum++], rules[i][j][k]);
                }
            }
        }
    }

    for(int i=0;i<NTNum;i++)
    {
        char LTemp = hashStrToChar(NT[i]);
        if(i==0)
        {
            symbolStart = LTemp;
        }
        int ind = LTemp;
        char ruleTemp[maxCap];
        mapping[ind]=1;
        int check_cnt=0;
        for(int j=0;j<rulesNT[i];j++)
        {
            
            for(int k=0;strlen(rules[i][j][k])>0; k++)
            {
            	if(rules[i][j][k][0]!=EPSILON)
                {
	                ruleTemp[check_cnt]=hashStrToChar(rules[i][j][k]);
            	}
                else
                {
            		ruleTemp[check_cnt]=EPSILON;
                }
                mapping[ruleTemp[check_cnt]]=1;
                check_cnt++;
            }
            ruleTemp[check_cnt]=NULLSPACE;
            strcpy(R[ind][count_R[ind]++], ruleTemp);
            check_cnt=0;
        }
        L[ind]=LTemp;
        check[ind]=1;
    }

    

    //display
    printf("Original Input Grammar : \n");
    for(int i=0;i<maxCap;i++)
    {
        if(check[i])
        {
            printf("    %s -> ", hashCharToString(L[i]));
            for(int j=0;j<count_R[i];j++){
                for(int k=0;k<(int)strlen(R[i][j]);k++)
                {
                    if(R[i][j][k]==EPSILON)
                    {
                        printf("? ");
                    }
                    else
                    {
                        printf("%s ", hashCharToString(R[i][j][k]));
                    }
                }
                if(j+1 < count_R[i])
                {
                    printf("| ");
                }
            }
            printf("\n");
        }
    }


    //
    for(int i=0;i<maxCap;i++)
    {
        if(check[i])
        {
            for(int j=0;j<count_R[i];j++)
            {
                char currTemp[maxCap];
                strcpy(currTemp, R[i][j]);
                if(isupper(R[i][j][0]) && R[i][j][0]<L[i])
                {
                    char cTemp = R[i][j][0];
                    int len = count_R[cTemp];
                    int k=0;
                    while(1)
                    {
                        char flagNewTemp[maxCap];
                        int cnt=0;
                        for(int l=0;l<(int)strlen(R[cTemp][k]);l++)
                        {
                            flagNewTemp[cnt++]=R[cTemp][k][l];
                        }
                        for(int l=1;l<(int)strlen(currTemp);l++)
                        {
                            flagNewTemp[cnt++]=currTemp[l];
                        }
                        flagNewTemp[cnt]=NULLSPACE;
                        if(k!=0)
                        {
                            strcpy(R[i][count_R[i]++], flagNewTemp);
                        }
                        else
                        {
                            strcpy(R[i][j], flagNewTemp);
                        }
                        k++;
                        if(k>=len)
                        {
                            break;
                        }
                    }
                }
            }
            int pointPivot = 0;
            for(int j=0;j<count_R[i];j++)
            {
                if(R[i][j][0] == L[i])
                {
                    char temp[maxCap];
                    strcpy(temp, R[i][j]);
                    strcpy(R[i][j], R[i][pointPivot]);
                    strcpy(R[i][pointPivot], temp);
                    pointPivot++;
                }
            }
            if(pointPivot > 0)
            {
                char temp[maxCap];
                strcpy(temp, hashCharToString(L[i]));
                strcat(temp, "1");
                strcpy(NT[NTNum++], temp);
                char curChar = hashStrToChar(temp);
                L[curChar] = curChar;
                check[curChar] = 1;
                int cur=0;
                for(int k=0;k<pointPivot;k++)
                {
                    char tempFlag[maxCap];
                    int cnt=0;
                    for(int l=1;l<strlen(R[i][k]);l++)
                    {
                        tempFlag[cnt++]=R[i][k][l];
                    }
                    tempFlag[cnt++]=curChar;
                    tempFlag[cnt]=NULLSPACE;
                    strcpy(R[curChar][count_R[curChar]++], tempFlag);
                    if(k==pointPivot-1)
                    {
                        tempFlag[1]=NULLSPACE;
                        tempFlag[0]=EPSILON;
                        strcpy(R[curChar][count_R[curChar]++], tempFlag);
                    }
                }
                for(int k=pointPivot;k<count_R[i];k++)
                {
                    char tempFlag[maxCap];
                    if(!strcmp(R[i][k], "?"))
                    {
                        tempFlag[1]=NULLSPACE;
                        tempFlag[0]=curChar;
                        strcpy(R[i][cur++], tempFlag);
                        continue;
                    }
                    strcpy(tempFlag, R[i][k]);
                    strncat(tempFlag, &curChar, 1);
                    strcpy(R[i][cur++], tempFlag);
                }
                if(pointPivot == count_R[i])
                {
                    char tempFlag[maxCap];
                    tempFlag[0]=curChar;
                    tempFlag[1]=NULLSPACE;
                    strcpy(R[i][cur++], tempFlag);
                }
                count_R[i]=cur;
            }
        }
    }
    
    
    //display
    printf("Grammar without left recursion : \n");
    for(int i=0;i<maxCap;i++)
    {
        if(check[i])
        {
            printf("    %s -> ", hashCharToString(L[i]));
            for(int j=0;j<count_R[i];j++){
                for(int k=0;k<(int)strlen(R[i][j]);k++)
                {
                    if(R[i][j][k]==EPSILON)
                    {
                        printf("? ");
                    }
                    else
                    {
                        printf("%s ", hashCharToString(R[i][j][k]));
                    }
                }
                if(j+1 < count_R[i])
                {
                    printf("| ");
                }
            }
            printf("\n");
        }
    }


    // int number=1;
    // printf("Enter number of input strings to be passed \n");
    // scanf("\n");
    // scanf("%d",&number);
    // printf("Enter strings one by one \n");
    // int counterInput = 0;
    for(;1;)
    {
        int check = scanf("%[^\n]%*c", rule);
        scanf("\n");

        if(check == -1)
        {
            break;
        }
        int len = strlen(rule);
        char temp[maxCap];
        rulesConvertedLength = 0;
        int cnt=0;

        for(int i=0;i<len;i++)
        {
            if(rule[i] == SPACE)
            {
                if(cnt)
                {
                    temp[cnt]=NULLSPACE;
                    rulesConverted[rulesConvertedLength++] = hashStrToChar(temp);
                }
                cnt=0;
            }
            else if(iscntrl(rule[i]) == 0)
            {
                temp[cnt++]=rule[i];
            }
        }
        if(cnt)
        {
            temp[cnt]=NULLSPACE;
            rulesConverted[rulesConvertedLength++] = hashStrToChar(temp);
        }
        currIndex = 0;
        rulesConverted[rulesConvertedLength]=NULLSPACE;
        printf("\n");
        int found = handle_check(symbolStart);
        if(!found || currIndex != rulesConvertedLength)
        {
            printf("\nCannot be generated : ");
        }
        else
        {
            printf("\nSuccessfully generated : ");
        }
        printf("%s\n\n", rule);
    }
	return 0;
}

