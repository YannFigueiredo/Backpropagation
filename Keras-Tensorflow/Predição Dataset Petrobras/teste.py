import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

base = pd.read_csv("dataset/petr4-treinamento.csv")
base = base.dropna()

base_treinamento = base.iloc[:, 1:2].values
normalizador = MinMaxScaler(feature_range=(0, 1))
base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)

print(base_treinamento)

print(base_treinamento_normalizada)