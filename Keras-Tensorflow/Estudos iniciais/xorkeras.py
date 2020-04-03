from keras.models import Sequential
from keras import optimizers
from keras.layers import Dense
import numpy as np
# fix random seed for reproducibility

# load pima indians dataset

# split into input (X) and output (Y) variables
input = np.array([[1,1],[1,0],[0,1],[0,0]])
output = np.array([[0],[1],[1],[0]])
# create model


model = Sequential()

model.add(Dense(6, input_dim=2, activation='sigmoid', use_bias=True))
model.add(Dense(1, activation='sigmoid',use_bias=True))

# Compile model
sgd = optimizers.SGD(momentum=0.1, lr=0.9, decay=0.0, nesterov=False)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(input, output, epochs=40000, batch_size=1)


# evaluate the model
scores = model.evaluate(input, output)
predicted = model.predict(input)
for i, predict in enumerate(predicted):
    print("predicted=> "+str(predict[0])+" - real => "+str(output[i][0]))


print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
