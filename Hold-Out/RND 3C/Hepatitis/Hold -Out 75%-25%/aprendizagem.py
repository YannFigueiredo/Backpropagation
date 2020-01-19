import var
import teste
import treino
import random
import numpy as np

#Define os valores de entrada e saída
def conjunto_treinamento(x, y):
  treino.criar_treino(x, y)  

#Inicializa os pesos w1 e w2
def inicializa_pesos(w1, w2):
  #aleartorio = random.randint(30, 41)
  #var.aleart = aleartorio
  random.seed(30)
  for i in range(0, var.NENT):
    for j in range(1, var.NINT):
      aleartorio = random.randint(1, 101)
      w1[i, j] = (1.0 - 2.0*aleartorio)/100.0
  for j in range(0, var.NINT):
    for k in range(0, var.NSAI):
      aleartorio = random.randint(1, 101)
      w2[j, k] = (1.0 - 2.0*aleartorio)/100.0

#Define os valores de h
def intermediaria(x, w1, h, m):
  h[0] = 1.0 #Bias

  for j in range(1, var.NINT):
    somatorio = 0.0
    for i in range(0, var.NENT):
      somatorio = somatorio + x[m,i]*w1[i,j]
    somatorio = -somatorio
    h[j] = 1.0/(1.0+np.exp(somatorio)) #Função de ativação

#Define o valor de o
def saida(h, w2, o):
  for k in range(0, var.NSAI):
    somatorio = 0.0
    for j in range(0, var.NINT):
      somatorio = somatorio + h[j]*w2[j,k]
    somatorio = -somatorio
    o[k] = 1.0/(1.0+np.exp(somatorio)) #Função de ativação

#Calcula o erro do valor obtido na saída
def erro_saida(o, y, m):
  somatorio = 0.0
  for k in range(0, var.NSAI):
    somatorio = somatorio + (o[k] - y[m,k])*(o[k] - y[m,k])
  erro = 0.5*somatorio

  return erro

#Calcula o erro obtido com base no w2
def erro2(o, y, m, delta2):
  for k in range(0, var.NSAI):
    delta2[k] = o[k]*(1.0 - o[k])*(y[m,k]-o[k])

#Calcula o erro obtido com base em w1
def erro1(h, delta2, w2, delta1):
  for j in range(1, var.NINT):
    somatorio = 0.0
    for k in range(0, var.NSAI):
      somatorio = somatorio + delta2[k]*w2[j,k]
    delta1[j] = h[j] * (1 - h[j]) * somatorio

#Ajusta os pesos w2
def ajusta2(w2, delta2, h):
  for j in range(0, var.NINT):
    for k in range(0, var.NSAI):
      w2[j,k] = w2[j,k] + var.TAPR * delta2[k] * h[j]

#Ajusta os pesos w1
def ajusta1(w1, delta1, x, m):
  for i in range(0, var.NENT):
    for j in range(1, var.NINT):
      w1[i,j] = w1[i,j] + var.TAPR * delta1[j] * x[m,i]

#Verifica a rede e grava os resultados no relat.txt   
def verifica(x, w1, w2, y, conteudo):
  h = np.zeros(var.NINTER)
  o = np.zeros(var.NSAI)
  cont = acertos = 0
  erro_grande = 0
  
  teste.criar_teste(x, y)

  for m in range(0, var.NPAD):
    intermediaria(x, w1, h, m)
    saida(h, w2, o)
    err = erro_saida(o, y, m)

    conteudo.append('Padrão>>'+str(m)+'\n')
    conteudo.append('Calculado>>'+str(o[0])+'\t\tDesejado>>'+str(y[m,0])+'\t\tErro>>'+str(err)+'\n')
    print('Padrão>>{}\n'.format(m))
    print('Calculado>>{}\t\tDesejado>>{}\t\tErro>>{:.9f}\n'.format(o[0], y[m,0], err))
    var.emq = var.emq + err
    var.emq = var.emq/var.NPAD
    
    #if err > 0.25: erro_grande += 1
   
    t = y[m, 0]
    e = o[0]
	 #Laços de acurácia manuais
    if t == 0.1 and e >= 0.05 and e < 0.15:
        acertos += 1
    elif t == 0.2 and e >= 0.15 and e <= 0.25:
        acertos += 1
  
  '''print('\nForam ignorados {} registros por conta de ter uma taxa de erro grande!\n'.format(erro_grande))
  var.NPAD -= erro_grande'''
  cont = var.NPAD - acertos

  print('emq>>{}'.format(var.emq))
  conteudo.append('\n\nErro Quadrático Médio>>'+str(var.emq)+'\n\n<<Pesos Camada Entrada Oculta>>')

  porcAcerto = (acertos/var.NPAD)*100

  print('\nPorcentagem de acertos: {:.2f}%\nAcertos: {}\nErros: {}'.format(porcAcerto, acertos, cont))

  #Tabulando
  tabela = []

  try:
    with open('tabela_hold_out_3C.csv', 'r') as f:
      pass
  except IOError: tabela.append('Erros,Acertos,NINT,TAPR,Épocas,Acurácia,EMQ\n')

  tabela.append(str(cont)+','+str(acertos)+','+str(var.NINT)+','+str(var.TAPR)+','+str(var.MAXITER)+','+str(porcAcerto)+'%,'+str(var.emq)+'\n')

  arquivo = open('tabela_hold_out_3C.csv', 'a')
  arquivo.writelines(tabela)
  arquivo.close()

  for i in range(0, var.NENT):
    for j in range(1, var.NINT):
      conteudo.append('\nw1['+str(i)+']['+str(j)+']='+str(w1[i,j]))
    conteudo.append('\n')
  
  conteudo.append('\n\n<<Pesos Camada Oculta Saída>>')
  for i in range(0, var.NINT):
    for j in range(0, var.NSAI):
      conteudo.append('\nw2['+str(i)+']['+str(j)+']='+str(w2[i,j]))
    conteudo.append('\n')
