#include<stdio.h>
#include<assert.h>

#define POLYSIZE 8192
typedef struct str_poly
{
	char poly[POLYSIZE];
	int length;
} strPoly;


strPoly dp[POLYSIZE];
strPoly mp[POLYSIZE];

int debug=0;

void printPoly( strPoly& a )
{
	int i;
	int j=0;
	for( i=a.length-1;i>0;i-- )
	{
		if(a.poly[i]!=0)
		{
			printf("%dX**%03d+",(int)a.poly[i],i);
			j++;
			if( j==8 )
			{
				j=0;
				printf("\n");
			}
		}
	}
	if( a.poly[0]!=0 && a.length!=0 )
		printf("%x",a.poly[0]);
}

void copyPoly( strPoly& a, strPoly& b )
{
	b.length=a.length;
	int i;
	for( i=0;i<b.length;i++ )
		b.poly[i]=a.poly[i];
}

void xk( strPoly& a, int k )
{
	a.length=k+1;
	for( int i=0;i<k;i++ )
	{
		a.poly[i]=0;
	}
	a.poly[k]=1;
}

void pdiv( strPoly& a, strPoly& b, strPoly& d )
{

	int i,j;
	d.length=a.length+1-b.length;
	assert( b.poly[b.length-1]==1 );
	for( i=a.length-1;i>=b.length-1;i-- )
	{
		d.poly[i-b.length+1]=a.poly[i];
		if( a.poly[i]==1 )
			for( j=0;j<b.length-1;j++ )
				a.poly[i-j-1]^=b.poly[b.length-2-j];
	}
	a.length=b.length-1;
	for( i=a.length-1;i>=0;i-- )
	{
		if( a.poly[i]!=0 )
		{
			a.length=i+1;
			break;	
		}
	}
	if( i==-1 )
		a.length=0;
}

void padd( strPoly& a, strPoly& b, strPoly& c )
{
	strPoly d;
	int i,j;
	if( a.length>b.length )	
	{
		copyPoly(a,d);
		for( i=0;i<b.length;i++ )
			d.poly[i]^=b.poly[i];	
	}
	else
	{
		copyPoly(b,d);
		for( i=0;i<a.length;i++ )
			d.poly[i]^=a.poly[i];	
	}
	for( i=d.length-1;i>=0;i-- )
	{
		if( d.poly[i]!=0 )
		{
			d.length=i+1;
			break;	
		}
	}
	if( i==-1 )
		d.length=0;
	copyPoly(d,c);
}
void pmul( strPoly& a, strPoly& b, strPoly& c )
{

	int i,j;
	strPoly d;
	d.length=a.length+b.length-1;
	if( debug==2 )
	{
		printf("\nMul: a");
		printPoly(a);
		printf("\nMul: b");
		printPoly(b);
			
	}	
	for( i=0;i<d.length;i++)
		d.poly[i]=0;
	for( i=0;i<b.length;i++ )
	{
		for( j=0;j<a.length;j++ )
			d.poly[i+j]^=(a.poly[j]&b.poly[i]);
	}
	if( debug==2 )
	{
		printf("\nMul: c");
		printPoly(d);
		printf("\n");
			
	}	
	copyPoly(d,c);
}


int findp( strPoly dpp[], int p )
{
	strPoly a,b,c,d;
	int i,j,l,k;
	
	xk(a,p);
	a.poly[0]=1;

	i=3;
	l=0;
#if	DEBUGLEVEL>25
		printPoly(a);
		printf("\n");
#endif
	while(i<0x80000000)
	{
		
		k=i;
		b.length=0;
		for(;k!=0;k>>=1)
		{
			b.poly[b.length]=k&1;
			b.length++;
		}
		for(k=0;k<l;k++)
		{
			copyPoly(b,d);
			pdiv(d,dpp[k],c);
			if( c.length==0 )
				break;
		}
		while( k==l )
		{
			copyPoly(a,d);
			pdiv(d,b,c);
			if( d.length!=0 )
				break;
			copyPoly(b,dpp[l]);
			l++;
			copyPoly(c,a);
		}
		if( a.length<b.length )
			break;
		i++;
	}
	
	return l;	
	
}

int rdiv( strPoly& a, strPoly& b, strPoly& m, strPoly& n)
{
	
	if( debug==1 )
	{
		printf("\n a:\n");
		printPoly( a );
		printf("\n b:\n");
		printPoly( b );
	}
	strPoly dl[127];
	strPoly g1,g2,g3;
	strPoly *pg1,*pg2,*pg3;
	strPoly *mk0,*mk1,*mk2;
	int i,j,k;
	
	copyPoly(b,g3);
	copyPoly(a,g2);
	pg1=&g1;
	pg2=&g2;
	pg3=&g3;
	i=0;
	strPoly *t;
	
	while( pg3->length != 1 )	
	{
		t=pg1;
		pg1=pg2;
		pg2=pg3;
		pg3=t;
		if( debug==1 )
		{
			printf("\ndiv1:");
			printPoly(*pg1);
			printf("\ndiv1:");
			printPoly(*pg2);
		}
		pdiv(*pg1,*pg2,dl[i]);
		if( debug==1 )
		{
			printf("\nd[%d]:",i);
			printPoly(dl[i]);
			printf("\nrem:");
			printPoly(*pg1);
			printf("\n");
		}
		copyPoly(*pg1,*pg3);
		i++;
		if( pg3->length==0 )
		{
			copyPoly(*pg2,m);
			return -1;
		}
	}
	
	mk2=&g3;
	mk1=&g2;
	mk0=&g1;
	
	mk2->length=1;
	mk2->poly[0]=1;
	
	copyPoly( dl[i-1], *mk1 );
	copyPoly( *mk2, n );
	copyPoly( *mk1, m );
	
	for( j=i-2;j>=0;j-- )
	{
		if( debug==1 )
		{
			printf("\nmk2:");
			printPoly(*mk2);
			printf("\nmk1:");
			printPoly(*mk1);
			printf("\nl[%d]:",j);
			printPoly(dl[j]);
			printf("\n");
		}
		pmul( *mk1,dl[j],*mk0);
		if( debug==1 )
		{
			printf("\nbefore add mk0:");
			printPoly(*mk0);
			printf("\n");
		}
		padd( *mk0, *mk2, *mk0 );
		if( debug==1 )
		{
			printf("\nmk0:");
			printPoly(*mk0);
			printf("\n");
		}
		copyPoly( *mk1, n );
		copyPoly( *mk0, m );
		t=mk2;
		mk2=mk1;
		mk1=mk0;
		mk0=t;
	}
	
	if( debug==1 )
	{	
		printf("\n m:\n");
		printPoly( m );
		printf("\n n:\n");
		printPoly( n );
	}
	return 0;	
		
}
int main( int argc, char *argv[] )
{
	int i,k,l,j;
	int p;
	
	sscanf(argv[1],"%d",&p);
	
	int num = findp( dp, p );	
	
	strPoly a,m,n,b,c,e;
	
	a.length=1;
	a.poly[0]=1;

	for( i=0;i<num;i++ )
	{
		a.length=1;
		a.poly[0]=1;
		for( j=0;j<num;j++ )
		{
			if( i!=j )
			{	
				pmul(a,dp[j],a);
			}
		}
		m.length=0;
		n.length=0;
		rdiv(a,dp[i],m,n);
		pmul(n,a,e);
		pmul(m,dp[i],b);
		padd(e,b,c);
		if( c.length!=1 && c.poly[0]!=1 )
		{
			printf("\nc:");
			printPoly(c);
			printf("\n");
		}
		copyPoly(n,mp[i]);
	}
	for( i=0;i<num;i++ )
	{
		k=0;
		for(j=0;j<dp[i].length;j++)
			if(dp[i].poly[j]==1)
				k|=(1<<j);
		printf("0x%x, ",k);
		k=0;
		for(j=0;j<mp[i].length;j++)
			if(mp[i].poly[j]==1)
				k|=(1<<j);
		printf("0x%x, \n",k);
	}

	return 0;
}