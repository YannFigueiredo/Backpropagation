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
'''for i in range(len(dados)):
    print('DADOS LINHA {}: {}\n'.format(i ,dados[i]))'''

NPAD = 1000
NENT = 24
NSAI = 1

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

#Cálculo de mediana
dados_q1 = dados_q3 = 0
cont = True
def calc_mediana(intervalo):
  global dados_q1
  global dados_q3
  global cont
  if len(intervalo) % 2 == 0:
    mediana = (intervalo[(len(intervalo)//2)-1]+intervalo[len(intervalo)//2])/2
    if cont == True:
      dados_q1 = (len(intervalo)//2)-1
      dados_q3 = len(intervalo)//2
  else:
    mediana = intervalo[len(intervalo)//2]
    if cont == True:    
      dados_q1 = (len(intervalo)//2)-1
      dados_q3 = (len(intervalo)//2)+1
  return mediana

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l

atributos = [1, 3, 9] #Atributos de interesse

#Criando uma cópia ordenada do primeiro atributo de interesse
atr = []
atr1 = []
for i in range(NPAD):
	atr.append(int(dados[i][atributos[0]]))
atr1 = sorted(atr)
print(atr1)

mediana = calc_mediana(atr1)
cont = False

#Cálculos estatísticos do atributo 1
q1 = calc_mediana(atr1[:dados_q1+1])
q3 = calc_mediana(atr1[dados_q3:])
iq = q3-q1
lim_inf = q1 - 1.5*iq
lim_sup = q3 + 1.5*iq
print('Mediana = {}\nQ1 = {}\nQ3 = {}\nIQ = {}\nLimite inferior = {}\nLimite superior = {}'.format(mediana, q1, q3, iq, lim_inf, lim_sup))

#Verificando outliers do atributo 1
linhas1 = []
for i in range(len(dados)):
  if atr[i] > lim_sup or atr[i] < lim_inf:
    linhas1.append(i)

'''print(linhas1)
print(len(linhas1))'''

#Criando uma cópia ordenada do segundo atributo de interesse
cont = True
atr = []
atr1 = []
for i in range(NPAD):
	atr.append(int(dados[i][atributos[1]]))
atr1 = sorted(atr)
print(atr1)

mediana = calc_mediana(atr1)
cont = False

#Cálculos estatísticos do atributo 2
q1 = calc_mediana(atr1[:dados_q1+1])
q3 = calc_mediana(atr1[dados_q3:])
iq = q3-q1
lim_inf = q1 - 1.5*iq
lim_sup = q3 + 1.5*iq
print('Mediana = {}\nQ1 = {}\nQ3 = {}\nIQ = {}\nLimite inferior = {}\nLimite superior = {}'.format(mediana, q1, q3, iq, lim_inf, lim_sup))

#Verificando outliers do atributo 2
linhas2 = []
for i in range(len(dados)):
  if atr[i] > lim_sup or atr[i] < lim_inf:
    linhas2.append(i)

'''print(linhas2)
print(len(linhas2))'''

#Criando uma cópia ordenada do terceiro atributo de interesse
cont = True
atr = []
atr1 = []
for i in range(NPAD):
	atr.append(int(dados[i][atributos[2]]))
atr1 = sorted(atr)
print(atr1)

mediana = calc_mediana(atr1)
cont = False

#Cálculos estatísticos do atributo 3
q1 = calc_mediana(atr1[:dados_q1+1])
q3 = calc_mediana(atr1[dados_q3:])
iq = q3-q1
lim_inf = q1 - 1.5*iq
lim_sup = q3 + 1.5*iq
print('Mediana = {}\nQ1 = {}\nQ3 = {}\nIQ = {}\nLimite inferior = {}\nLimite superior = {}'.format(mediana, q1, q3, iq, lim_inf, lim_sup))

#Verificando outliers do atributo 3
linhas3 = []
for i in range(len(dados)):
  if atr[i] > lim_sup or atr[i] < lim_inf:
    linhas3.append(i)

'''print(linhas3)
print(len(linhas3))'''

#Montando a lista definitiva de linhas com outliers
linhas = linhas1+linhas2+linhas3
linhas = remove_repetidos(linhas)
linhas = sorted(linhas, reverse = True)
print(linhas)
print(len(linhas))

#Removendo outliers
for i in range(len(linhas)):
  del dados[linhas[i]]

#Criando novo dataset
dados_tratados = []
for i in range(len(dados)):
  for j in range(NENT):
    dados_tratados.append(dados[i][j]+',')
  for k  in range(NSAI):
    dados_tratados.append(dados[i][-1])
  dados_tratados.append('\n')

print(len(dados_tratados))
    
arq = open('german_credit_sem_outliers.txt', 'w')
arq.writelines(dados_tratados)
arq.close()

#Construindo um dataset.arff sem outliers
arq = open('german-credit.arff', 'r')
arq_arff = arq.readlines()

for i in range(len(linhas)):
  del arq_arff[linhas[i]]

arq = open('german-credit-sem-outliers.arff', 'w')
arq.writelines(arq_arff)
arq.close()