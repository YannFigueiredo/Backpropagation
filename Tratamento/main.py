import numpy as np
import random
import re
from itertools import chain
from collections import Counter

def organizar_dados():
    aux = np.zeros((len(var.x_treino)+len(var.x_teste), var.NSAI))
    i = 0
    for j in range(len(var.y_treino)):
        for k in range(var.NSAI):
            aux[i, k] = var.y_treino[j, k]
            i+=1

    for j in range(len(var.y_teste)):
        for k in range(var.NSAI):
            aux[i, k] = var.y_teste[j, k]
            i+=1

    contador1 = Counter(chain.from_iterable(var.y_treino))
    contador2 = Counter(chain.from_iterable(var.y_teste))

    print('Treino: {}; Teste: {}'.format(contador1, contador2))

aleat = False

arquivo = 'german-numeric.txt'

arq = open(arquivo, 'r')
texto = arq.readlines()
arq.close()

if aleat == True:
  arq = open(arquivo, 'w')
  random.shuffle(texto)
  arq.writelines(texto)
  arq.close()
  arq = open(arquivo, 'r')
  texto = arq.readlines()
  arq.close()
'''  
for i in range(len(texto)): 
    texto[i] = re.sub('   ', ',' , texto[i])

for i in range(len(texto)): 
    texto[i] = re.sub('  ', ',' , texto[i])
    texto[i] = texto[i][1:-2]'''
 
'''print(texto[0])
print(type(texto[0]))
print(texto[0][1])'''

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
print(len(dados[0]))
print(type(dados[0][0]))

#Removendo espaços
for i in range(len(dados)):
    for j in range(24):
        print(j)
        dados[i][j] = dados[i][j].strip()
for i in range(len(dados)):
    dados[i][-1] = dados[i][-1].strip()
for i in range(len(dados)):
    print('DADOS LINHA {}: {}\n'.format(i ,dados[i]))

NPAD = 1000
NENT = 25
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

#Normalizando os dados
  for i in range(NPAD):
    for j in range(1,NENT):
       aux = str(x[i,j])
       aux = aux.replace(".", "")
       if aux[0] == '0': aux = aux[1:]
       aux = '0.'+aux
       x[i, j] = float(aux)

  for i in range(NPAD):
    for j in range(NSAI):
       aux = str(y[i, j])
       aux = aux.replace(".", "")
       if aux[0] == '0': aux = aux[1:]        
       aux = '0.' + aux
       y[i, j] = float(aux)

for i in range(NPAD):
	for j in range(NSAI):
		if y[i, j] == 0.1:
			y[i, j] = 0.0
		else: y[i, j] = 1.0
dataset = []
print('Valores de Entrada\n')
dataset.append('def criar_dataset(x, y):\n')
#dataset.append('Valores de Entrada\n\n')
for i in range(NPAD):
  for j in range(NENT):
    print('x[{}][{}] = {};'.format(i, j, x[i,j]))
    dataset.append('\tx['+str(i)+']['+str(j)+'] = '+str(x[i,j])+';\n')
  print('\n')
  dataset.append('\n')

cont1 = cont2 = 0
#dataset.append('Valores de Saída\n\n')
print('\nValores de saída\n')
for i in range(NPAD):
  for j in range(NSAI):
    print('y[{}][{}] = {};'.format(i, j, y[i,j]))
    if y[i, j] == 0.1: cont1 += 1
    else: cont2 += 1
    dataset.append('\ty['+str(i)+']['+str(j)+'] = '+str(y[i,j])+';\n')

print('Contador 1: {}\nContador 2: {}'.format(cont1, cont2))

contador = Counter(chain.from_iterable(y))

print('Contador:',contador)
arq = open('dataset.py', 'w')
arq.writelines(dataset)
