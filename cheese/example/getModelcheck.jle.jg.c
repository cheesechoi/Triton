#include <stdio.h>



int main(int argc, char* argv[])
{
	char test = argv[1][0];

	if( 'A' < test && test < 'Z' )
		printf("done!");
	else
		printf("nope!");
	return 0;
}
