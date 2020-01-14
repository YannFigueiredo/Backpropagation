import var
import random
import treino
import teste
import numpy as np
import aprendizagem

#Inicializando as matrizes e vetores
x = np.zeros((var.NPAD, var.NENT)) #Matriz das entradas
h1 = np.zeros(var.NINTER) #Vetor da intermediária
h2 = np.zeros(var.NINTER) #Vetor da intermediária
o = np.zeros(var.NSAI) #Vetor do resultado obtido na saída
y = np.zeros((var.NPAD, var.NSAI)) #Matriz da saída
delta = np.zeros(var.NINTER)
delta1 = np.zeros(var.NINTER) #Valor com  base no erro ENT->INT
delta2 = np.zeros(var.NSAI) #Valor com  base no erro INT->SAI
w1 = np.zeros((var.NENT, var.NINTER)) #Peso ENT->INT1
w2 = np.zeros((var.NINTER, var.NSAI)) #Peso INT2->SAI
w3 = np.zeros((var.NINT1, var.NINT2)) #Peso INT1->INT2
m = l = 0 #m = índice de controle, l = contador de iterações
erromax = var.ACEITAVEL*2.0 #Erro máximo

#var.NPAD = 666 #Número de padrões para treino

#Criando a variável de texto para ser gravada posteriormente em relat.txt
arq = open('relat.txt', 'w')
arq.writelines('')
arq.close()
arq = open('relat.txt', 'r')
conteudo = arq.readlines()
arq.close()

conteudo.append("Aprendizagem da Rede\n\n")
print('Aprendizagem da Rede\n')

aprendizagem.conjunto_treinamento(x, y)
aprendizagem.inicializa_pesos(w1, w2, w3)

'''print('Valores de Entrada\n')
for i in range(len(x)):
  for j in range(var.NENT):
    print('x[{}][{}] = {};'.format(i, j, x[i,j]))
  print('\n')

print('\nValores de saída\n')
for i in range(len(y)):
  for j in range(var.NSAI):
    print('y[{}][{}] = {};'.format(i, j, y[i,j]))'''

while(erromax > var.ACEITAVEL and l < var.MAXITER):
  acertos = cont = 0
  
  if m == var.NPAD: m = 0
  aprendizagem.intermediaria(x, w1, h1, m)
  aprendizagem.intermediaria2(w3, h1, h2, m)
  aprendizagem.saida(h2, w2, o)
  err = aprendizagem.erro_saida(o, y, m)
  if(err > erromax): erromax = err
  aprendizagem.erro2(o, y, m, delta2)
  aprendizagem.erro1(h2, delta2, w2, delta1)
  aprendizagem.erroN(h1, delta1, w3, delta)
  aprendizagem.ajusta2(w2, delta2, h2)
  aprendizagem.ajusta1(w1, delta, x, m)
  aprendizagem.ajusta(w3, delta1, h1, m)
  l += 1
  
  print('\nPadrão>>{}\t\tÉpoca>>{}\t\tErro>>{}'.format(m, l, err))
  m += 1

var.NPAD = 288 #Número de padrões para o teste
conteudo.append('\n\nVERIFICAÇÃO\n')
print('\n\nVERIFICAÇÃO\n')
aprendizagem.verifica(x, w1, w2, w3, y, conteudo)

arq = open('relat.txt', 'w')
arq.writelines(conteudo)
arq.close()

