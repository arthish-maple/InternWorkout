# -*- coding: utf-8 -*-
"""Heart_Classification_using_Neural_Network.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xZQeHN1iiiB23FyX-upH1ThSSG1BX-ZK
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

heart_data = pd.read_csv("/content/heart.csv")
heart_data.head()

heart_data.shape

"""## Data Preprocessing"""

heart_data.info()

heart_data.describe()

heart_data = heart_data[heart_data['ca'] < 4] #drop the wrong ca values
heart_data = heart_data[heart_data['thal'] > 0] # drop the wong thal value
print(f'The length of the data now is {len(heart_data)} instead of 303!')

heart_data = heart_data.rename(
    columns = {'cp':'chest_pain_type',
               'trestbps':'resting_blood_pressure',
               'chol': 'cholesterol',
               'fbs': 'fasting_blood_sugar',
               'restecg' : 'resting_electrocardiogram',
               'thalach': 'max_heart_rate_achieved',
               'exang': 'exercise_induced_angina',
               'oldpeak': 'st_depression',
               'slope': 'st_slope',
               'ca':'num_major_vessels',
               'thal': 'thalassemia'},
    errors="raise")

#visualize

plt.figure(figsize = (18,12))
sns.heatmap(heart_data.corr() , annot=True, cmap='coolwarm', fmt='.1f', linewidths=2, linecolor='lightgrey')
plt.suptitle('Correlation Matrix', fontsize=38, y=1)
plt.show()

heart_data['target'].unique()

"""## Splitting the data"""

X = heart_data.drop("target" , axis = 1)
y = heart_data['target']

X_train , X_test , y_train , y_test = train_test_split(X , y ,test_size = 0.3 , random_state = 4 , stratify = y )
print(X.shape ,X_train.shape , X_test.shape )

"""# scaling"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)

X_test_std = scaler.transform(X_test)

"""## Building Model"""

import tensorflow as tf
import keras
from keras import layers
from keras import models
from keras import utils
from keras.layers import Dense
from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Activation
from keras.regularizers import l2
from keras.optimizers import SGD

np.random.seed(3)

#tuning the optimizer
epochs=60
lr = 0.1
decay_rate = lr / epochs
momentum = 0.8

sgd = SGD(learning_rate=lr,weight_decay= decay_rate, momentum=momentum, nesterov=False)

input_dim = X_train_std.shape[1]

lr_model = Sequential()
lr_model.add(Dense(64, activation=tf.nn.relu, kernel_initializer='uniform',
                input_dim = input_dim))
lr_model.add(Dropout(0.1))
lr_model.add(Dense(64, kernel_initializer='uniform', activation=tf.nn.relu))
lr_model.add(Dense(2, kernel_initializer='uniform', activation=tf.nn.sigmoid))

# compile the model
lr_model.compile(loss='sparse_categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

lr_model_history = lr_model.fit(X_train, y_train,
                    batch_size=32,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(X_test, y_test))

# Plot the loss function
fig, ax = plt.subplots(1, 1, figsize=(10,6))
ax.plot(np.sqrt(lr_model_history.history['loss']), 'r', label='train')
ax.plot(np.sqrt(lr_model_history.history['val_loss']), 'b' ,label='val')
ax.set_xlabel(r'Epoch', fontsize=20)
ax.set_ylabel(r'Loss', fontsize=20)
ax.legend()
ax.tick_params(labelsize=20)