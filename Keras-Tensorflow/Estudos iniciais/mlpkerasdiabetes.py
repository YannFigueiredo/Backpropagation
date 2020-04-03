from keras.models import Sequential
from keras import optimizers
from keras.layers import Dense
import numpy
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load pima indians dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
# create model

model = Sequential()

model.add(Dense(12, input_dim=8, activation='relu'))

model.add(Dense(8,  activation='relu'))
model.add(Dense(1, activation='relu'))
# Compile model
sgd = optimizers.SGD(momentum=0.1, lr=0.9, decay=0.0, nesterov=False)
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
# Fit the model
model.fit(X, Y, nb_epoch=1050, batch_size=10)

# evaluate the model
scores = model.evaluate(X, Y)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
