from __future__ import absolute_import
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

import datetime
import json

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils

from ini_caltech101.keras_extensions.normalization import BatchNormalization

'''
    Test the BatchNormalization on a simple deep NN with the MNIST dataset.

'''

batch_size = 60
nb_classes = 10
nb_epoch = 50

batch_normalization = True

# the data, shuffled and split between tran and test sets
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype("float32")
X_test = X_test.astype("float32")
X_train /= 255
X_test /= 255
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()
model.add(Dense(100, init='he_normal', input_shape=(784,)))
if batch_normalization:
    model.add(BatchNormalization(mode=1))
model.add(Activation('sigmoid'))
model.add(Dense(100, init='he_normal'))
if batch_normalization:
    model.add(BatchNormalization(mode=1))
model.add(Activation('sigmoid'))
model.add(Dense(100, init='he_normal'))
if batch_normalization:
    model.add(BatchNormalization(mode=1))
model.add(Activation('sigmoid'))
model.add(Dense(nb_classes, init='he_normal'))
model.add(Activation('softmax'))

sgd = SGD(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

hist = model.fit(X_train, Y_train, batch_size=batch_size, nb_epoch=nb_epoch, show_accuracy=True, verbose=2, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, show_accuracy=True, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])

dt = datetime.datetime.now()
open('results/{:%Y-%m-%d_%H.%M.%S}_mnist-bn_architecture.json'.format(dt), 'w').write(model.to_json())
open('results/{:%Y-%m-%d_%H.%M.%S}_mnist-bn_history.json'.format(dt), 'w').write(json.dumps(hist.history))
open('results/{:%Y-%m-%d_%H.%M.%S}_mnist-bn_test-score.json'.format(dt), 'w').write(json.dumps(score))