import var
import teste
import treino
import random
import numpy as np

#Define os valores de entrada e saída
def conjunto_treinamento(x, y):
    treino.criar_treino(x, y)

#Inicializa os pesos w1 e w2
def inicializa_pesos(w1, w2, w3):
  #aleartorio = random.randint(30, 41)
  #var.aleart = aleartorio
  random.seed(30)
  for i in range(0, var.NENT):
    for j in range(1, var.NINT1):
      aleartorio = random.randint(1, 101)
      w1[i, j] = (1.0 - 2.0*aleartorio)/100.0
  for j in range(0, var.NINT2):
    for k in range(0, var.NSAI):
      aleartorio = random.randint(1, 101)
      w2[j, k] = (1.0 - 2.0*aleartorio)/100.0
  for j in range(0, var.NINT1):
    for k in range(0, var.NINT2):
      aleartorio = random.randint(1, 101)
      w3[j, k] = (1.0 - 2.0*aleartorio)/100.0

#Define os valores de h1
def intermediaria(x, w1, h1, m):
  h1[0] = 1.0 #Bias

  for j in range(1, var.NINT1):
    somatorio = 0.0
    for i in range(0, var.NENT):
      somatorio = somatorio + x[m,i]*w1[i,j]
    somatorio = -somatorio
    h1[j] = 1.0/(1.0+np.exp(somatorio)) #Função de ativação

#Define os valores de h2
def intermediaria2(w3, h1, h2, m):
  h2[0] = 1.0 #Bias

  for j in range(1, var.NINT2):
    somatorio = 0.0
    for i in range(0, var.NINT1):
      somatorio = somatorio + h1[i]*w3[i,j]
    somatorio = -somatorio
    h2[j] = 1.0/(1.0+np.exp(somatorio)) #Função de ativação

#Define o valor de o
def saida(h2, w2, o):
  for k in range(0, var.NSAI):
    somatorio = 0.0
    for j in range(0, var.NINT2):
      somatorio = somatorio + h2[j]*w2[j,k]
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
def erro1(h2, delta2, w2, delta1):
  for j in range(1, var.NINT2):
    somatorio = 0.0
    for k in range(0, var.NSAI):
      somatorio = somatorio + delta2[k]*w2[j,k]
    delta1[j] = h2[j] * (1 - h2[j]) * somatorio

#Calcula o erro obtido com base em w3
def erroN(h1, delta1, w3, delta):
  for j in range(1, var.NINT1):
    somatorio = 0.0
    for k in range(0, var.NINT2):
      somatorio = somatorio + delta1[k]*w3[j,k]
    delta[j] = h1[j] * (1 - h1[j]) * somatorio

#Ajusta os pesos w2
def ajusta2(w2, delta2, h2):
  for j in range(0, var.NINT2):
    for k in range(0, var.NSAI):
      w2[j,k] = w2[j,k] + var.TAPR1 * delta2[k] * h2[j]

#Ajusta os pesos w1
def ajusta1(w1, delta, x, m):
  for i in range(0, var.NENT):
    for j in range(1, var.NINT1):
      w1[i,j] = w1[i,j] + var.TAPR1 * delta[j] * x[m,i]

#Ajusta os pesos w3
def ajusta(w3, delta1, h1, m):
  for i in range(0, var.NINT1):
    for j in range(1, var.NINT2):
      w3[i,j] = w3[i,j] + var.TAPR * delta1[j] * h1[i]

#Verifica a rede e grava os resultados no relat.txt   
def verifica(x, w1, w2, w3, y, conteudo):
  h1 = np.zeros(var.NINTER)
  h2 = np.zeros(var.NINTER)
  o = np.zeros(var.NSAI)
  cont = acertos = 0

  teste.criar_teste(x, y)

  for m in range(0, var.NPAD):
    intermediaria(x, w1, h1, m)
    intermediaria2(w3, h1, h2, m)
    saida(h2, w2, o)
    err = erro_saida(o, y, m)

    conteudo.append('Padrão>>'+str(m)+'\n')
    conteudo.append('Calculado>>'+str(o[0])+'\t\tDesejado>>'+str(y[m,0])+'\t\tErro>>'+str(err)+'\n')
    print('Padrão>>{}\n'.format(m))
    print('Calculado>>{}\t\tDesejado>>{}\t\tErro>>{:.9f}\n'.format(o[0], y[m,0], err))
    var.emq = var.emq + err

    t = y[m, 0]
    e = o[0]

    #Laços de acurácia manuais
    if t == 0.1 and e >= 0.05 and e < 0.15:
      acertos += 1
    elif t == 0.2 and e >= 0.15 and e < 0.25:
      acertos += 1
    '''elif t == 0.3 and e >= 0.25 and e < 0.35:
      acertos += 1'''

    cont = var.NPAD - acertos

    var.emq = var.emq/var.NPAD
  print('emq>>{}'.format(var.emq))
  conteudo.append('\n\nErro Quadrático Médio>>'+str(var.emq)+'\n\n<<Pesos Camada Entrada Oculta>>')

  porcAcerto = (acertos/var.NPAD)*100

  print('\nPorcentagem de acertos: {:.2f}%\nAcertos: {}\nErros: {}'.format(porcAcerto, acertos, cont))

  for i in range(0, var.NENT):
    for j in range(1, var.NINT1):
      conteudo.append('\nw1['+str(i)+']['+str(j)+']='+str(w1[i,j]))
    conteudo.append('\n')
  
  conteudo.append('\n\n<<Pesos Camada Oculta Saída>>')
  for i in range(0, var.NINT2):
    for j in range(0, var.NSAI):
      conteudo.append('\nw2['+str(i)+']['+str(j)+']='+str(w2[i,j]))
    conteudo.append('\n')

  conteudo.append('\n\n<<Pesos Camada Oculta 1 - Oculta 2>>')
  for i in range(0, var.NINT1):
    for j in range(0, var.NINT2):
      conteudo.append('\nw3['+str(i)+']['+str(j)+']='+str(w3[i,j]))
    conteudo.append('\n')
