#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define MAXN 128
static const char *KA = "KRYPTOSABCDEFGHIJLMNQUVWXZ";
int kai[26], N, ncrib;
int cAZ[MAXN], cKA[MAXN];
int qpos[MAXN], pAZ[MAXN], pKA[MAXN];
long hits = 0, tested = 0;
int part = 0, nparts = 1;
char curlabel[320] = "";

static inline int kv(int v,int ca,int ck,int pa,int pk){
  switch(v){
    case 0: return (ca-pa+26)%26; case 1: return (ca+pa)%26; case 2: return (pa-ca+26)%26;
    case 3: return (ck-pk+26)%26; case 4: return (ck+pk)%26; case 5: return (pk-ck+26)%26;
    case 6: return (ck-pa+26)%26; case 7: return (ca-pk+26)%26;
    case 8: return (ck+pa)%26;   default: return (ca+pk)%26;
  }
}
#define NV 10
int minR, maxP;
static void check(const int *f, int w, const int *perm, int orient){
  for(int model=1; model<=2; model++){
    for(int v=0; v<NV; v++){
      int keypos[MAXN], key[MAXN];
      for(int k=0;k<ncrib;k++){
        int j=f[qpos[k]];
        keypos[k] = (model==1)? qpos[k] : j;
        key[k] = kv(v,cAZ[j],cKA[j],pAZ[k],pKA[k]);
      }
      for(int p=2;p<=maxP;p++){
        int slot[64]; for(int i=0;i<p;i++) slot[i]=-1;
        int red=0, bad=0;
        for(int k=0;k<ncrib;k++){
          int r=keypos[k]%p;
          if(slot[r]<0) slot[r]=key[k];
          else if(slot[r]!=key[k]){bad=1;break;}
          else red++;
        }
        tested++;
        if(!bad && red>=minR){
          hits++;
          if(curlabel[0]) printf("HIT route=%s",curlabel);
          else { printf("HIT w=%d perm=",w); for(int i=0;i<w;i++)printf("%d",perm[i]); }
          printf(" orient=%d model=%d variant=%d period=%d redundant=%d key=",orient,model,v,p,red);
          for(int i=0;i<p;i++){ if(slot[i]<0)putchar('?'); else putchar(v>=3&&v<=5? KA[slot[i]] : 'A'+slot[i]); }
          putchar('\n');
        }
      }
    }
  }
}
static void process(int w,const int *perm){
  int order[MAXN], n=0;
  for(int ci=0;ci<w;ci++){int col=perm[ci]; for(int idx=col; idx<N; idx+=w) order[n++]=idx;}
  int jof[MAXN]; for(int j=0;j<N;j++) jof[order[j]]=j;
  check(jof,w,perm,0);
  check(order,w,perm,1);
}
static void process_raw(const int *order){
  int jof[MAXN]; for(int j=0;j<N;j++) jof[order[j]]=j;
  check(jof,0,NULL,0);
  check(order,0,NULL,1);
}
static int dw_max = 0;
static const int *curA;
static char baselabel[160];
static void emit_pair(int w,const int *perm){
  int B[MAXN], n=0, T[MAXN];
  for(int ci=0;ci<w;ci++){int col=perm[ci]; for(int idx=col; idx<N; idx+=w) B[n++]=idx;}
  char dig[64]; int dl=0; for(int i=0;i<w&&dl<60;i++) dl+=snprintf(dig+dl,sizeof(dig)-dl,"%d",perm[i]);
  for(int j=0;j<N;j++) T[j]=curA[B[j]];
  snprintf(curlabel,sizeof curlabel,"%s+route-then-col(w=%d,perm=%s)",baselabel,w,dig); process_raw(T);
  for(int j=0;j<N;j++) T[j]=B[curA[j]];
  snprintf(curlabel,sizeof curlabel,"%s+col-then-route(w=%d,perm=%s)",baselabel,w,dig); process_raw(T);
}
static void perm_rec(int w,int *a,int k){
  if(k==w){emit_pair(w,a);return;}
  for(int i=k;i<w;i++){int t=a[k];a[k]=a[i];a[i]=t; perm_rec(w,a,k+1); t=a[k];a[k]=a[i];a[i]=t;}
}
static long splitcnt=0;
static void permute(int w,int *a,int k){
  int sk = (w<2)?w:2;
  if(k==sk && nparts>1){ if((splitcnt++ % nparts)!=part) return; }
  if(k==w){process(w,a);return;}
  for(int i=k;i<w;i++){ int t=a[k];a[k]=a[i];a[i]=t; permute(w,a,k+1); t=a[k];a[k]=a[i];a[i]=t;}
}
int main(int argc,char**argv){
  FILE*fp=fopen(argv[1],"r"); int maxW=atoi(argv[2]); maxP=atoi(argv[3]); minR=atoi(argv[4]);
  for(int i=0;i<26;i++) kai[(int)KA[i]-'A']=i;
  char buf[512]; fgets(buf,512,fp); N=strlen(buf); while(N&&(buf[N-1]=='\n'||buf[N-1]=='\r'))N--;
  for(int i=0;i<N;i++){cAZ[i]=buf[i]-'A'; cKA[i]=kai[cAZ[i]];}
  ncrib=0; int pos; char s[256];
  while(fscanf(fp,"%d %255s",&pos,s)==2){
    for(int i=0;s[i];i++){qpos[ncrib]=pos-1+i; pAZ[ncrib]=s[i]-'A'; pKA[ncrib]=kai[pAZ[ncrib]]; ncrib++;}
  }
  fprintf(stderr,"N=%d cribs=%d\n",N,ncrib);
  if(argc>6 && !strcmp(argv[6],"permfile")){
    FILE*pf=fopen(argv[7],"r"); int w; long cnt=0;
    while(fscanf(pf,"%d",&w)==1){ int a[64]; for(int i=0;i<w;i++) fscanf(pf,"%d",&a[i]); process(w,a); cnt++; }
    fprintf(stderr,"perms=%ld tested=%ld hits=%ld\n",cnt,tested,hits); return 0;
  }
  if(getenv("DOUBLE_W")) dw_max=atoi(getenv("DOUBLE_W"));
  if(argc>6 && !strcmp(argv[6],"rawperm")){
    FILE*pf = strcmp(argv[7],"-") ? fopen(argv[7],"r") : stdin; long cnt=0; int order[MAXN];
    while(fscanf(pf,"%159s",curlabel)==1){
      for(int i=0;i<N;i++) if(fscanf(pf,"%d",&order[i])!=1) return 1;
      process_raw(order); cnt++;
      if(dw_max>=2){ strncpy(baselabel,curlabel,sizeof baselabel-1); curA=order;
        for(int w=2;w<=dw_max;w++){ int a[16]; for(int i=0;i<w;i++)a[i]=i; perm_rec(w,a,0); } }
    }
    fprintf(stderr,"routes=%ld tested=%ld hits=%ld\n",cnt,tested,hits); return 0;
  }
  if(getenv("NPARTS")){nparts=atoi(getenv("NPARTS")); part=atoi(getenv("PART"));}
  if(part==0){ int a[1]={0}; process(1,a); }
  int minW = argc>5 ? atoi(argv[5]) : 2; for(int w=minW; w<=maxW; w++){ int a[16]; for(int i=0;i<w;i++)a[i]=i; splitcnt=0; permute(w,a,0); fprintf(stderr,"w=%d done, tested=%ld hits=%ld\n",w,tested,hits);}
  fprintf(stderr,"TOTAL tested=%ld hits=%ld\n",tested,hits);
}
