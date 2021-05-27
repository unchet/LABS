                   // for program  to_lab13.cpp
#define N 26

char A='A';
char Z='Z';
char a='a';
char z='z';

char Alph[2*N];  // alphabet: small and capital letters


int Letter(char c)
{
	return c >= a&&c <= z || c >= A&&c <= Z;
}


int CreateSet(char W[], char S[])
{
	char c; int i;
	for (i = 0; i < N; i++)S[i] = S[N + i] = 0;
	for (i = 0; c = W[i]; i++)
		if (c >= a&&c <= z) {
			S[c - a] = 1;
		}
		else
			if (c >= A&&c <= Z) {
				S[N + c - A] = 1;
			}
}

int DisplaySet(char S[])
{
	Alph[0] = a; Alph[N] = A; Alph[2 * N] = 0; // alphabet fills up
	for (int i = 1; i < N; i++)
	{
		Alph[i] = Alph[i - 1] + 1;
		Alph[i + N] = Alph[i + N - 1] + 1;
	}        // --"--
	printf("\n%s\n", Alph);            // and prints
	for (int i = 0; i < 2 * N; i++)
		printf("%1d", S[i]); printf("\n");  // set prints
}

int EqualSet(char S1[], char S2[])
{
	for (int i = 0; i < 2 * N; i++)
		if (S1[i] != S2[i]) return 0;
	return 1;
}

int UnionSet(char S1[], char S2[], char S3[])
{
	for (int i = 0; i < 2 * N; i++) {
		S3[i] = S1[i] || S2[i];
	}
}

int IntersSet(char S1[], char S2[], char S3[])
{
	for (int i = 0; i < 2 * N; i++) {
		S3[i] = S1[i] && S2[i];
	}
}

int IncludeSet(char S1[], char S2[])
{
	for (int i = 0; i < 2 * N; i++)
		if (S1[i] == 1 && S2[i] == 0) return 0;
	return 1;
}

int EmptySet(char S[])
{
	for (int i = 0; i < 2 * N; i++)
		if (S[i] == 1) return 0;
	return 1;
}

int InSet(char c, char S[])              // add to set
{
	if (Letter(c)) {
		if (c >= a) S[c - a] = 1;
	}
    else S[c+N-A]=1;
}
