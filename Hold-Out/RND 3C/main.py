import re
import var
import random
import numpy as np
import aprendizagem

#Inicializando as matrizes e vetores
x = np.zeros((var.NPAD, var.NENT)) #Matriz das entradas
h = np.zeros(var.NINTER) #Vetor da intermediária
o = np.zeros(var.NSAI) #Vetor do resultado obtido na saída
y = np.zeros((var.NPAD, var.NSAI)) #Matriz da saída
delta1 = np.zeros(var.NINTER) #Valor com  base no erro ENT->INT
delta2 = np.zeros(var.NSAI) #Valor com  base no erro INT->SAI
w1 = np.zeros((var.NENT, var.NINTER)) #Peso ENT->INT
w2 = np.zeros((var.NINTER, var.NSAI)) #Peso INT->SAI
m = l = 0 #m = índice de controle, l = contador de iterações
erromax = var.ACEITAVEL*2.0 #Erro máximo

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
aprendizagem.inicializa_pesos(w1, w2)

'''print('Valores de Entrada\n')
for i in range(len(x)):
  print(x[i])

print('\nValores de saída\n')
for i in range(len(y)):
  print(y[i])
'''

while(erromax > var.ACEITAVEL and l < var.MAXITER):
  if m == var.NPAD: m = 0
  aprendizagem.intermediaria(x, w1, h, m)
  aprendizagem.saida(h, w2, o)
  err = aprendizagem.erro_saida(o, y, m)
  if(err > erromax): erromax = err
  aprendizagem.erro2(o, y, m, delta2)
  aprendizagem.erro1(h, delta2, w2, delta1)
  aprendizagem.ajusta2(w2, delta2, h)
  aprendizagem.ajusta1(w1, delta1, x, m)
  l += 1

  print('\nPadrão>>{}\t\tÉpoca>>{}\t\tErro>>{}'.format(m, l, err))
  m += 1

conteudo.append('\n\nVERIFICAÇÃO\n')
print('\n\nVERIFICAÇÃO\n')
var.NPAD = 288
aprendizagem.verifica(x, w1, w2, y, conteudo)

arq = open('relat.txt', 'w')
arq.writelines(conteudo)
arq.close()

