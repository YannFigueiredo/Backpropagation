dados_q1 = dados_q3 = 0
def mediana(intervalo):
  global dados_q1
  global dados_q3
  if len(intervalo) % 2 == 0:
    mediana = (intervalo[(len(intervalo)//2)-1]+intervalo[len(intervalo)//2])/2
    if dados_q1 or dados_q3 == 0:
      dados_q1 = (len(intervalo)//2)-1
      dados_q3 = len(intervalo)//2
  else:
    mediana = intervalo[len(intervalo)//2]
    if dados_q1 or dados_q3 == 0:    
      dados_q1 = dados_q3 = len(intervalo)//2
  return mediana

dados = [501, 504, 493, 499, 497, 503, 525, 495, 506, 502]
copia_dados = sorted(dados)

print(copia_dados)
mediana = mediana(copia_dados)

#Criando sub grupo de dados para o cálculo dos quartis
copia_q1 = []
copia_q3 = []
for i in range(0, dados_q1+1):
  copia_q1.append(copia_dados[i])
for i in range(dados_q3, len(copia_dados)):
  copia_q3.append(copia_dados[i])

#Cálculos estatísticos
q1 = mediana(copia_q1)
q3 = mediana(copia_q3)
iq = q3-q1
print('Mediana = {}\nQ1 = {}\nQ3 = {}\nIQ = {}'.format(mediana, q1, q3, iq))
