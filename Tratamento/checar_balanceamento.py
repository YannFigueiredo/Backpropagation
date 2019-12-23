import teste
import treino
import d1
import numpy as np
from itertools import chain
from collections import Counter

NENT = 25
NSAI = 1

x = np.zeros((250, NENT))
y = np.zeros((250, NSAI))

d1.criar_d1(x, y)

contador = Counter(chain.from_iterable(y))

print(contador)

'''x = np.zeros((334, NENT))
y = np.zeros((334, NSAI))

teste.criar_teste(x, y)

contador = Counter(chain.from_iterable(y))

print(contador)'''

