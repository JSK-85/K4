#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define MAXN 128
static const char *KA="KRYPTOSABCDEFGHIJLMNQUVWXZ", *AZ="ABCDEFGHIJKLMNOPQRSTUVWXYZ";
int kai[26], N, ncrib, maxP, minR;
char C[MAXN]; int has[MAXN], pl[MAXN];
static inline int kv(int v,int ca,int ck,int pa,int pk){
  switch(v){
    case 0: return (ca-pa+26)%26; case 1: return (ca+pa)%26; case 2: return (pa-ca+26)%26;
    case 3: return (ck-pk+26)%26; case 4: return (ck+pk)%26; case 5: return (pk-ck+26)%26;
    case 6: return (ck-pa+26)%26; case 7: return (ca-pk+26)%26;
    case 8: return (ck+pa)%26;   default: return (ca+pk)%26; }
}
long hits=0,tested=0;
static void testkeys(int n,int *pos,int *ca,int *ck,int *pa,int *pk,const char*tag,int m[4],int off,int ha){
  for(int v=0;v<10;v++){
    int key[MAXN];
    for(int k=0;k<n;k++) key[k]=kv(v,ca[k],ck[k],pa[k],pk[k]);
    for(int p=2;p<=maxP;p++){
      int slot[64]; for(int i=0;i<p;i++)slot[i]=-1; int red=0,bad=0;
      for(int k=0;k<n;k++){int r=pos[k]%p; if(slot[r]<0)slot[r]=key[k]; else if(slot[r]!=key[k]){bad=1;break;} else red++;}
      tested++;
      if(!bad&&red>=minR){hits++; printf("HIT %s alph=%s off=%d M=[[%d,%d],[%d,%d]] variant=%d period=%d redundant=%d key=",tag,ha?"KA":"AZ",off,m[0],m[1],m[2],m[3],v,p,red);
        for(int i=0;i<p;i++){ if(slot[i]<0)putchar('?'); else putchar(v>=3&&v<=5?KA[slot[i]]:'A'+slot[i]); } putchar('\n');}
    }
  }
}
int main(int argc,char**argv){
  FILE*fp=fopen(argv[1],"r"); maxP=atoi(argv[2]); minR=atoi(argv[3]);
  for(int i=0;i<26;i++)kai[i]=0; for(int i=0;i<26;i++)kai[KA[i]-'A']=i;
  char buf[512]; if(!fgets(buf,512,fp))return 1; N=strlen(buf); while(N&&(buf[N-1]=='\n'||buf[N-1]=='\r'))N--; memcpy(C,buf,N);
  int pos; char s[256]; memset(has,0,sizeof has);
  while(fscanf(fp,"%d %255s",&pos,s)==2) for(int i=0;s[i];i++){has[pos-1+i]=1; pl[pos-1+i]=s[i]-'A';}
  for(int ha=0;ha<2;ha++){ const char*H= ha?KA:AZ; int hidx[26]; for(int i=0;i<26;i++)hidx[H[i]-'A']=i;
   for(int off=0;off<2;off++){
    int bl[MAXN],nb=0; for(int b=off;b+1<N;b+=2) if(has[b]&&has[b+1]) bl[nb++]=b;
    for(int m0=0;m0<26;m0++)for(int m1=0;m1<26;m1++)for(int m2=0;m2<26;m2++)for(int m3=0;m3<26;m3++){
      int det=((m0*m3-m1*m2)%26+26)%26; if(det%2==0||det%13==0) continue;
      int m[4]={m0,m1,m2,m3};
      int pos2[MAXN],ca[MAXN],ck[MAXN],pa[MAXN],pk[MAXN],n;
      n=0;
      for(int bI=0;bI<nb;bI++){int b=bl[bI]; int a=hidx[C[b]-'A'], c=hidx[C[b+1]-'A'];
        int y[2]={(a*m0+c*m2)%26,(a*m1+c*m3)%26};
        for(int i=0;i<2;i++){ int L=H[y[i]]-'A'; pos2[n]=b+i; ca[n]=L; ck[n]=kai[L]; pa[n]=pl[b+i]; pk[n]=kai[pa[n]]; n++; } }
      testkeys(n,pos2,ca,ck,pa,pk,"H1(Hill(Vig(P)))",m,off,ha);
      n=0;
      for(int bI=0;bI<nb;bI++){int b=bl[bI]; int a=hidx[pl[b]+0], c=hidx[pl[b+1]];
        int z[2]={(a*m0+c*m2)%26,(a*m1+c*m3)%26};
        for(int i=0;i<2;i++){ int L=H[z[i]]-'A'; pos2[n]=b+i; int cc=C[b+i]-'A'; ca[n]=cc; ck[n]=kai[cc]; pa[n]=L; pk[n]=kai[L]; n++; } }
      testkeys(n,pos2,ca,ck,pa,pk,"H2(Vig(Hill(P)))",m,off,ha);
    }}}
  fprintf(stderr,"tested=%ld hits=%ld\n",tested,hits);
}
