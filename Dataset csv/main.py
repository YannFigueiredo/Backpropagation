import numpy as np
import random
import re

arquivo = 'german-numeric.txt'

arq = open(arquivo, 'r')
texto = arq.readlines()
arq.close()

#Modelando os dados do arquivo txt
dados = []
for i in range(len(texto)):
  dados.append(re.split('  |,|\n|-', texto[i]))
  dados[i] = dados[i][1:]
  #print(re.split(' ,|\n', texto[i]))
  #if i != len(texto) - 1:
  del (dados[i][-1])
#print(dados)
arq = open('dados.txt', 'w')
arq.writelines(str(dados))
#print(len(dados[0]))
#print(type(dados[0][0]))

#Removendo espaços
for i in range(len(dados)):
    for j in range(24):
        #print(j)
        dados[i][j] = dados[i][j].strip()
for i in range(len(dados)):
    dados[i][-1] = dados[i][-1].strip()
for i in range(len(dados)):
    print('DADOS LINHA {}: {}\n'.format(i ,dados[i]))

NPAD = 1000
NENT = 24
NSAI = 1
x = np.zeros((NPAD, NENT)) #Matriz das entradas
y = np.zeros((NPAD, NENT)) #Matriz das saídas

#Excluindo registros vazios
while True:
  cont = 0
  for i in range(len(dados)):
    if '?' in dados[i]:
      del dados[i]
      cont +=1
    if cont > 0:
      break
  if cont == 0:
    break
'''
#Definindo x
k = 1
for i in range(NPAD):
  for j in range(0, NENT-1):
    x[i, k] = float(dados[i][j])
    k += 1
  k = 1
  x[i, 0] = 1.0

#Definindo y
for i in range(NPAD):
  for j in range(NSAI):
    y[i, j] = float(dados[i][-1])

dataset = []
dataset.append('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20')
for i in range(NPAD):
  for j in range(NENT):
    dataset.append(str(x[i,j])+',')
  for k in range(NSAI):
    dataset.append(str(y[i,j]))
  dataset.append('\n')'''

dataset = []
dataset.append('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25\n')
for i in range(NPAD):
  for j in range(NENT):
    dataset.append(dados[i][j]+',')
  for k in range(NSAI):
    dataset.append(dados[i][-1])
  dataset.append('\n')

arq = open('dataset.csv', 'w')
arq.writelines(dataset)
