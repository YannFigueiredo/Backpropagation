#include <fstream>
#include <iostream>
#include <math.h>
#include <iomanip>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "treino.hpp"
#include "teste.hpp"


using namespace std;

const int NENT = 20;
const int NINT = 5;
const int NSAI = 1;
int NPAD = 53;
unsigned long MAXITER = 450000;
const double TAPR = 0.7;
const double ACEITAVEL = 0.0001;
double op[NSAI];
int verifica =0;
double emq=0.0;
 
ofstream fout("RELAT.txt");
void conjunto_treinamento1(double x[][NENT],double y[][NSAI]);
//pesos w3 que sao os pesos das realimentacoes
void inicializa_pesos(double w1[][NINT],double w2[][NSAI],double w3[][NINT]);
void intermediaria(double x[][NENT],double w1[][NINT],double h[],int m,double w3[][NINT],int t);
void saida(double h[],double w2[][NSAI],double

[]);
void erro_saida(double o[],double y[][NSAI],double& erro,int m);
void erro2(double o[],double y[][NSAI],int m,double delta2[]);
void erro1(double h[],double delta2[],double w2[][NSAI],double delta1[],double delta3[]);
void ajusta2(double w2[][NSAI],double delta2[],double h[]);
void ajusta1(double w1[][NINT],double delta1[],double x[][NENT],int m,double w3[][NINT],double delta3[],double o[]);
void verifica1(double x[][NENT],double w1[][NINT],double w2[][NSAI],double y[][NSAI],double w3[][NINT],int t);
void imprimir_vetor(double vetor[], int tamanho);
void imprimir_matriz(double matriz[][NSAI],int linhas,int colunas);


int main()
{
   double x[NPAD][NENT],h[NINT],hp[NINT],o[NSAI],y[NPAD][NSAI],delta1[NINT],delta2[NSAI],w1[NENT][NINT],w2[NINT][NSAI],erro,erromax,w3[NSAI][NINT],delta3[NINT];
   unsigned long l;
   int m;
   system("cls");
   int cont,t=0;
   cout << "\nAPRENDIZAGEM\n";
   conjunto_treinamento1(x,y);
   inicializa_pesos(w1,w2,w3);
   erromax = ACEITAVEL*2.0;
   m = 0;
   l = 0;
   while(erromax > ACEITAVEL && l < MAXITER)
     {
      if(m == NPAD) m = 0;
      intermediaria(x,w1,h,m,w3,t);
      t++;
      saida(h,w2,o);
      erro_saida(o,y,erro,m);
      if(erro > erromax) erromax = erro;
      erro2(o,y,m,delta2);
      erro1(h,delta2,w2,delta1,delta3);
      ajusta2(w2,delta2,h);
      ajusta1(w1,delta1,x,m,w3,delta3,o);
      l = l + 1;
      cout << "\npadrao  " << m;
       m = m + 1;
      cont++;
      cout << '\n' << l << "  Erro:  " << erro;
      //fout<<"\n";
      //fout<<erro;
     }
     //getch();
     NPAD = 27;
     cout << "\n\nVERIFICACAO\n";
     fout << "\n\nVERIFICACAO\n";
     verifica1(x,w1,w2,y,w3,t);
     //getch();
}

void conjunto_treinamento1(double x[][NENT],double y[][NSAI])
{
  criar_treino(x, y);
}

void inicializa_pesos(double w1[][NINT],double w2[][NSAI],double w3[][NINT])
{
   int i,j,k;
   double aleatorio;
   for(i=0;i<NENT;i++)
     for(j=1;j<NINT;j++)
       {
	aleatorio = (rand()%101);
	w1[i][j] =  (1.0 - 2.0 * aleatorio) / 100.0;
       }
   for(j=0;j<NINT;j++)
     for(k=0;k<NSAI;k++)
       {
	aleatorio = (rand()%101);
        w2[j][k] = (1.0 - 2.0 * aleatorio) / 100;
       
       }
   //ok
   for(k=0;k<NSAI;k++)
     for(j=0;j<NINT;j++)
       {
   	aleatorio = (rand()%101);
        w3[k][j] = (1.0 - 2.0 * aleatorio)/100;
       }
}

void intermediaria(double x[][NENT],double w1[][NINT],double h[],int m,double w3[][NINT],int t)
{
  int i,j,k;
  long double somatorio,somatorio1,somatorio2;
  somatorio=0;
  somatorio1=0;
  somatorio2=0;
  h[0]=1.0;
  //t=0
  //no instante t=0 as realimentacoes tem valor zero
  if(t==0)
   {
    for(j=0;j<NSAI;j++)
     {
      op[j]=0;
     }
   }
   for(j=1;j<NINT;j++)
   {
    somatorio=0.0;
    for(i=0;i<NENT;i++)
    {
     //ok
     somatorio=somatorio+x[m][i]*w1[i][j];
    }
    //parcela relativa as realimentacoes, para t=0 as parcelas sao zero como assumido pelo
    //vetor op[j]
    for(k=0;k<NSAI;k++)
    {
    //ok
     somatorio1=somatorio1+op[k]*w3[k][j];
    }
   // ok
    somatorio2=-(somatorio+somatorio1);
    //a saida h[j] agora recebe a contribuicao tambem das realimentacoes que e somatorio1
    h[j]=1.0/(1.0+exp(somatorio2));
   }
}


void saida(double h[],double w2[][NSAI],double o[])
{
   int j,k;
   double somatorio;
   for(k=0;k<NSAI;k++)
   {
     somatorio = 0.0;
     for(j=0;j<NINT;j++)
	somatorio = somatorio + h[j] * w2[j][k];
      somatorio = - somatorio;
    o[k] = 1.0 / (1.0 + exp(somatorio));
   }
   if(verifica==1)
    {
     for(k=0;k<NSAI;k++)
     {
       op[k]=o[k];
     }
    }

}

void erro_saida(double o[],double y[][NSAI],double& erro,int m)
{
   int k,cont;
   double somatorio;
   somatorio = 0.0;
   for(k=0;k<NSAI;k++)
     somatorio = somatorio + (o[k] - y[m][k]) * (o[k] - y[m][k]);
   erro = 0.5 * somatorio;
}

void erro2(double o[],double y[][NSAI],int m,double delta2[])
{
 int k;
 for(k=0;k<NSAI;k++)
  {
   //DELTA2-OK
   delta2[k]=o[k]*(1.0-o[k])*(y[m][k]-o[k]);

  }
}

void erro1(double h[],double delta2[],double w2[][NSAI],double delta1[],double delta3[])
  {
   int j,k;
   double somatorio,somatorio1;
   double soma;
   soma=0;
   for(k=0;k<NSAI;k++)
    {
     soma=soma+op[k];
    }
    for(j=1;j<NINT;j++)
     {
      somatorio = 0.0;
      somatorio1= 0.0;
      for(k=0;k<NSAI;k++)
      {
       somatorio=somatorio   + delta2[k] * w2[j][k];
       somatorio1=somatorio1 + delta2[k] * w2[j][k]*soma;
      }
      delta1[j]= h[j] * (1 - h[j]) * somatorio;
      delta3[j]= h[j] * (1 - h[j]) * somatorio1;
     }
  }

void ajusta2(double w2[][NSAI],double delta2[],double h[])
{
   int j,k;
   for(j=0;j<NINT;j++)
     for(k=0;k<NSAI;k++)
       w2[j][k] = w2[j][k] + TAPR * delta2[k] * h[j];

}

void ajusta1(double w1[][NINT],double delta1[],double x[][NENT],int m,double w3[][NINT],double delta3[],double o[])
{
   int i,j,k;
   for(i=0;i<NENT;i++)
    {
     for(j=1;j<NINT;j++)
      {
        w1[i][j] = w1[i][j] + TAPR * delta1[j] * x[m][i];
      }
    }
   for(i=0;i<NSAI;i++)
    {
      for(j=1;j<NINT;j++)
       {
	 w3[i][j]=w3[i][j] + TAPR * delta3[j];
       }
    }
   for(k=0;k<NSAI;k++)
    {
     op[k]=o[k];
    }
  
 }

void verifica1(double x[][NENT],double w1[][NINT],double w2[][NSAI],double y[][NSAI],double w3[][NINT],int t)
  {
   int m,k,i,j;
   int cont, acertos = 0, acertos1 = 0, acertos2 = 0, acertos3 = 0, acertos4 = 0;
   double erro,h[NINT],o[NSAI];

	criar_teste(x, y);

	for(k=0;k<NSAI;k++)
	{
	op[k]=0;
	verifica=1;
	}
	
	for(m=0;m<NPAD;m++) {
		intermediaria(x,w1,h,m,w3,t);
		saida(h,w2,o);
		erro_saida(o,y,erro,m);
		cout << "\nPadrao Testes>>" << m;
		cout << "\ncalculado>>" << o[0] << "  \tdesejado>>" << y[m][0] << "   \tErro>>" << erro;
		
		fout << "\nPadrao Testes>>" << m;
		fout << "\ncalculado>>" << o[0] << "  \tdesejado>>" << y[m][0] << "   \tErro>>" << erro;
		
		emq=emq+erro;
		
		double t = y[m][0];
		double e = o[0];
		
		if(t == 0.1 && e >= 0.05 && e < 0.15) {
			acertos1++;
		}else if(t == 0.2 && e >= 0.15 && e <= 0.25) {
			acertos2++;
		}/*else if(t == 0.6 && e >= 0.45 && e < 0.75) {
			acertos3++;
		}else if(t == 0.9 && e >= 0.75 && e < 1.05) {
			acertos4++;
		}	*/	
	}
	
	acertos = acertos1 + acertos2;
	cont = NPAD - acertos;	
	emq=emq/NPAD;
	float porcAcerto = (float) acertos / NPAD * 100.0;
	//printf("\nemq>>%f",emq);
	
	cout<<"\nContagem de acertos:>> " << acertos << "(" << acertos1 << ", " << acertos2 << ")";
	cout<<"\nContagem de erro:>> " << cont;
	cout<<"\nPorcentagem de acertos:>> " << porcAcerto;
	cout<<"\nAcuracia:>> " << ((float) acertos / NPAD);
	cout<<"\nEMQ>>"<<emq;
	
	fout<<"\n\nContagem de acertos:>> " << acertos << "(" << acertos1 << ", " << acertos2<<")";
	fout<<"\nContagem de erro:>> " << cont;
	fout<<"\nPorcentagem de acertos:>> " << porcAcerto;
	fout<<"\nAcuracia:>> " << ((float) acertos / NPAD);
  }

void imprimir_vetor(double vetor[], int tamanho)
  {
  int i;
  cout << "\nConjunto: ";
  cout << setprecision(4);
  for(i=0;i<tamanho;i++)
    cout << setw(6) << vetor[i] << ' ';
  }

void imprimir_matriz(double matriz[][NSAI],int linhas,int colunas)
  {
   int i,j;
   cout << setprecision(4);
   for(i=0;i<linhas;i++)
     {
      cout << '\n';
      for(j=0;j<colunas;j++)
	 cout << setw(6) << matriz[i][j] << ' ';
     }
  }
