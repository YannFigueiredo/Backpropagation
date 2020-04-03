from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout, LSTM, Flatten
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from keras import metrics

import keras.backend as K


def load_dataset(dataset, type):
    data = dataset
    data_y = data[type]
    data_x = data.drop(["Pesado", "Medio", "Leve"], axis=1)
    data_x = data_x.drop(["DiaInicio", "MesInicio", "AnoInicio",
                          "DiaFinal", "MesFinal", "AnoFinal"], axis=1)

    return data_x, data_y


x_train, y_train = load_dataset(pd.read_csv(
    'dataset/north_12_steps_train.csv', encoding='utf-8', delimiter=';'), 'Pesado')
x_test,  y_test = load_dataset(pd.read_csv(
    'dataset/north_12_steps_test.csv', encoding='utf-8', delimiter=';'), 'Pesado')

url = 'heavy'
regiao = 'southeast'

len_dataset = len(y_test) + len(y_train)
num_steps = int(len(y_test)/2)
total_by_num_steps = len_dataset-(num_steps)


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def cal_diff_mape(y_real, y_pred):
    return np.abs((y_real - y_pred) / y_real)


def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))


base_treinamento = x_train
base_treinamento_y = y_train
normalizador_entrada = MinMaxScaler(feature_range=(0, 1))
normalizador_saida = MinMaxScaler(feature_range=(0, 1))

base_treinamento_normalizada = normalizador_entrada.fit_transform(
    base_treinamento)
base_treinamento_normalizada_y = normalizador_entrada.fit_transform(np.array(
    base_treinamento_y).reshape(-1, 1))  # normalizador.fit_transform(base_treinamento_y)


# np.ndarray(shape=(381-90,90,5))
previsores = np.arange(total_by_num_steps*num_steps*5)
# np.ndarray(shape=(381-90,1,5))
preco_real = np.arange(total_by_num_steps*1*1)
previsores = previsores.reshape(total_by_num_steps, num_steps, 5)
preco_real = preco_real.reshape(total_by_num_steps, 1)

lista_previsores = []
lista_preco_real = []

for i in range(num_steps, total_by_num_steps-num_steps):
    lista_previsores.append(base_treinamento_normalizada[i-num_steps:i, :])
    lista_preco_real.append(base_treinamento_normalizada_y[i])


lista_previsores, lista_preco_real = np.array(
    lista_previsores), np.array(lista_preco_real)

# padrão (batch_size, timestep, column)

lista_previsores = np.reshape(
    lista_previsores, (lista_previsores.shape[0], lista_previsores.shape[1], 5))


regressor = Sequential()


regressor.add(LSTM(units=100, return_sequences=True,
                   input_shape=(lista_previsores.shape[1], 5)))
regressor.add(LSTM(units=100, return_sequences=False))
regressor.add(Dense(units=1, activation='linear'))

regressor.compile(optimizer='rmsprop', loss='mean_squared_error',
                  metrics=[metrics.mean_absolute_error, metrics.mean_absolute_percentage_error, rmse, 'accuracy'])


regressor.fit(lista_previsores, lista_preco_real,
              epochs=2000, batch_size=32, verbose=0)


# print(base_treinamento_normalizadda)

print('working...')


base_test = x_test
base_test_y = y_test
base_test_normalizada = normalizador_entrada.fit_transform(base_test)
base_test_normalizada_y = normalizador_entrada.fit_transform(
    np.array(base_test_y).reshape(-1, 1))

# previsores_test = np.arange((len_dataset-total_by_num_steps)*num_steps*5) # np.ndarray(shape=(381-90,90,5))
# preco_real_test = np.arange((len_dataset-total_by_num_steps)*1*1) #  np.ndarray(shape=(381-90,1,5))
# previsores_test = previsores_test.reshape(len_dataset-total_by_num_steps, num_steps, 5)
# preco_real_test = preco_real_test.reshape(len_dataset-total_by_num_steps, 1)

lista_previsores_test = []
lista_preco_real_test = []

for i in range(0, num_steps):
    lista_previsores_test.append(base_test_normalizada[i:num_steps+i, :])
    lista_preco_real_test.append(base_test_normalizada_y[num_steps+i])


lista_previsores_test, lista_preco_real_test = np.array(
    lista_previsores_test), np.array(lista_preco_real_test)

# padrão (batch_size, timestep, column)

lista_previsores_test = np.reshape(
    lista_previsores_test, (lista_previsores_test.shape[0], lista_previsores_test.shape[1], 5))

eval = regressor.evaluate(lista_previsores_test,
                          lista_preco_real_test, batch_size=32)
#mape = mean_absolute_percentage_error(lista_preco_real_test, lista_previsores_test)
#print("EVAL - MAPE => "+str(mape))
print("PREV")
print("metrics=[ 'mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'root_mean_squared_error', 'accuracy' ")
print(str(eval))

pred_treino = regressor.predict(lista_previsores)
pred_treino = normalizador_entrada.inverse_transform(pred_treino)
lista_preco_real = normalizador_entrada.inverse_transform(lista_preco_real)


print("treino")
for i in range(len(lista_preco_real)):
    print("pred: "+str(pred_treino[i])+"  real: "+str(lista_preco_real[i]))

fig, ax = plt.subplots()
line1, = ax.plot(pred_treino, label='predito')
line2, = ax.plot(lista_preco_real, label='real')
ax.set(ylim=(-20, 150))
plt.legend()
# plt.show()
plt.tight_layout()
plt.savefig('figura1.png', dpi=100, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1,
            frameon=None, metadata=None)
plt.close()

pred_teste = regressor.predict(lista_previsores_test)
pred_teste = normalizador_entrada.inverse_transform(pred_teste)
lista_preco_real_test = normalizador_entrada.inverse_transform(
    lista_preco_real_test)

sum = 0
print("teste")
for i in range(len(lista_preco_real_test)):
    print("pred: "+str(pred_teste[i])+"  real: "+str(lista_preco_real_test[i]))
    sum += cal_diff_mape(lista_preco_real_test[i], pred_teste[i])

mape = (100 * sum) / len(lista_preco_real_test)

fig, ax = plt.subplots()
line1, = ax.plot(pred_teste, label='predito')
line2, = ax.plot(lista_preco_real_test, label='real')
ax.set(ylim=(-20, 150))
plt.legend()
# plt.show()
plt.tight_layout()
plt.savefig('figura1.png', dpi=100, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1,
            frameon=None, metadata=None)
plt.close()


todas_predicoes = np.concatenate((pred_treino, pred_teste), axis=None)
todos_precos_reais = np.concatenate(
    (lista_preco_real, lista_preco_real_test), axis=None)


fig, ax = plt.subplots()
line1, = ax.plot(todas_predicoes, label='predito')
line2, = ax.plot(todos_precos_reais, label='real')
ax.set(ylim=(-20, 150))
plt.legend()
# plt.show()
plt.tight_layout()
plt.savefig('figura1.png', dpi=100, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1,
            frameon=None, metadata=None)
plt.close()


print("PREV")
print("metrics=[ 'mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'root_mean_squared_error', 'accuracy' ")
metrics = {}
metrics['mean_squared_error'] = eval[0]
metrics['mean_absolute_error'] = eval[1]
metrics['mean_absolute_percentage_error'] = mape[0]
metrics['root_mean_squared_error'] = np.sqrt(eval[1])
metrics['accuracy'] = eval[4]
print(str(metrics))


def cal_sum_mape(y_real, y_pred):
    yield cal_diff_mape(y_real, y_pred)
