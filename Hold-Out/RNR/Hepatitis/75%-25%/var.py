import numpy as np

NINT = 5 #4 neurônios internos + 1 bias

NINTER = 50 #Limite para pesos
NENT = 20 #2 neurônios de entrada + bias
NSAI = 1 #1 neurônio de saída
NPAD = 53 #Número de padrões
TAPR = 0.9 #Taxa de aprendizagem
MAXITER = 200000 #Limite de iterações
ACEITAVEL = 0.0001 #Erro aceitável
op = np.zeros(NSAI)
emq = 0.0 #Erro médio quadrático
verifica = 0
