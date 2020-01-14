import numpy as np

NINT = 7 #4 neurônios internos + 1 bias

NINTER = 50 #Limite para pesos
NENT = 25 #2 neurônios de entrada + bias
NSAI = 1 #1 neurônio de saída
NPAD = 666 #Número de padrões
TAPR = 0.7 #Taxa de aprendizagem
MAXITER = 600000 #Limite de iterações
ACEITAVEL = 0.0001 #Erro aceitável
op = np.zeros(NSAI)
emq = 0.0 #Erro médio quadrático
verifica = 0
