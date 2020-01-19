import re
import var
import random
import numpy as np
import aprendizagem

#Inicializando as matrizes e vetores
x = np.zeros((var.NPAD, var.NENT)) #Matriz das entradas
h = np.zeros(var.NINT) #Vetor da intermediária
hp = np.zeros(var.NINT) #Vetor da intermediária
o = np.zeros(var.NSAI) #Vetor do resultado obtido na saída
y = np.zeros((var.NPAD, var.NSAI)) #Matriz da saída
delta1 = np.zeros(var.NINT) #Valor com  base no erro ENT->INT
delta2 = np.zeros(var.NSAI) #Valor com  base no erro INT->SAI
w1 = np.zeros((var.NENT, var.NINT)) #Peso ENT->INT1
w2 = np.zeros((var.NINT, var.NSAI)) #Peso INT2->SAI
w3 = np.zeros((var.NSAI, var.NINT)) #Peso INT1->INT2
m = l = 0 #m = índice de controle, l = contador de iterações
delta3 = np.zeros(var.NINT)
erromax = var.ACEITAVEL*2.0 #Erro máximo

#Criando a variável de texto para ser gravada posteriormente em relat.txt
arq = open('relat'+'-'+str(var.NINT)+'-'+str(var.TAPR)+'-'+str(var.MAXITER)+'.txt', 'w')
arq.writelines('')
arq.close()
arq = open('relat'+'-'+str(var.NINT)+'-'+str(var.TAPR)+'-'+str(var.MAXITER)+'.txt', 'r')
conteudo = arq.readlines()
arq.close()

conteudo.append("Aprendizagem da Rede\n\n")
print('Aprendizagem da Rede\n')

aprendizagem.conjunto_treinamento(x, y)
aprendizagem.inicializa_pesos(w1, w2, w3)

cont = t = erro = 0

while(erromax > var.ACEITAVEL and l < var.MAXITER):
  if m == var.NPAD: m = 0
  aprendizagem.intermediaria(x, w1, h, m, w3, t)
  t += 1
  aprendizagem.saida(h, w2, o)
  erro = aprendizagem.erro_saida(o, y, erro, m)
  if(erro > erromax): erromax = erro
  aprendizagem.erro2(o, y, m, delta2)
  aprendizagem.erro1(h, delta2, w2, delta1, delta3)
  aprendizagem.ajusta2(w2, delta2, h)
  aprendizagem.ajusta1(w1, delta1, x, m, w3, delta3, o)
  l += 1

  print('\nPadrão>>{}\t\tÉpoca>>{}\t\tErro>>{}'.format(m, l, erro))
  m += 1
  cont += 1
conteudo.append('\n\nVERIFICAÇÃO\n')
print('\n\nVERIFICAÇÃO\n')
var.NPAD = 27
aprendizagem.verifica(x, w1, w2, y, w3, t, conteudo)

arq = open('relat'+'-'+str(var.NINT)+'-'+str(var.TAPR)+'-'+str(var.MAXITER)+'.txt', 'w')
arq.writelines(conteudo)
arq.close()

