import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler

base = pd.read_csv("dataset/petr4-treinamento.csv")
base = base.dropna() #Remove as linhas onde há colunas com valores faltantes

#Normalização de dimensionamento de recursos
base_treinamento = base.iloc[:, 1:2].values
normalizador = MinMaxScaler(feature_range=(0, 1))
base_treinamento_normalizada = normalizador.fit_transform(base_treinamento)

#Criando uma estrutura de dados com 90 timesteps e 1 output
x_treino = []
y_treino = []

for i in range(90, 1242):
	x_treino.append(base_treinamento_normalizada[i-90:i, 0])
	y_treino.append(base_treinamento_normalizada[i, 0])
	x_treino, y_treino = np.array(x_treino), np.array(y_treino)

#Remodelando
x_treino = np.reshape(x_treino, (x_treino.shape[0], x_treino.shape[1], 1))

### Construindo o modelo RNN LSTM ###

#Inicializando o RNN
model = Sequential()

#Adicionado camadas LSTM e alguma regularização de Dropout
model.add(LSTM(units=50,return_sequences=True,input_shape=(x_treino.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1, activation='linear'))
model.compile(optimizer='adam',loss='mean_squared_error', metrics=['mean_absolute_error'])
model.fit(x_treino, y_treino, epochs=100, batch_size=32)

### Predição na base de teste ###

base_teste = pd.read_csv('dataset/petr4-teste.csv')
preco_real_teste = base_teste.iloc[:, 1:2].values

base_completa = pd.concat((base['Open'], base_teste['Open']), axis=0)

entradas = base_completa[len(base_completa) - len(base_teste)-90:].values
entradas = entradas.reshape(-1, 1)
entradas = normalizador.transform(entradas)

x_teste = []
for i in range(90, 112):
    x_teste.append(entradas[i-90:i, 0])

x_teste = np.array(x_teste)
x_teste = np.reshape(x_teste, (x_teste.shape[0], x_teste.shape[1], 1))

preco_predito = model.predict(x_teste)
preco_predito = normalizador.inverse_transform(preco_predito)