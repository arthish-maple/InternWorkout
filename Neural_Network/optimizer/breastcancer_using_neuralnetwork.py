# -*- coding: utf-8 -*-
"""BreastCancer_using_NeuralNetwork.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MUTvPWy86DHzxgi4wvQ5Q1ThwZnj_WTy
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.datasets
from sklearn.model_selection import train_test_split

"""Data Collection & Processing"""

#loading the data from sklearn
breast_cancer_dataset = sklearn.datasets.load_breast_cancer()

print(breast_cancer_dataset)  # data is i a form of a dictionary

#Loading the data to a data frame
data_frame = pd.DataFrame(breast_cancer_dataset.data, columns = breast_cancer_dataset.feature_names)

#print the first 5 rows of the dataframe
data_frame.head()

# adding the 'target' column to the data frame
data_frame['label'] = breast_cancer_dataset.target

#print last 5 rows of the dataframe
data_frame.tail()

#number of rows and columns in the dataset
data_frame.shape

#getting some inforamtion about the data
data_frame.info()

#checking for missing values
data_frame.isnull().sum()

#statistical measures about the data
data_frame.describe()

#checking the distribution of target variable
data_frame['label'].value_counts()

"""1 -> Benign ( doesn't travel to other parts of the body)



0 -> Malignant( travels to other parts of the body so cancerous)
"""

data_frame.groupby('label').mean()

"""Sperating the features and target"""

X = data_frame.drop (columns='label', axis=1)
Y = data_frame['label']

print(X)

print(Y)

"""Splitting the data into Training data & Testing data"""

X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size=0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

X_train

# Check feature names of input data before transformation
print("Input Feature Names:", X.columns)

X_test.to_csv("breast_test.csv",index=False)
from google.colab import files
#files.download("breast_test.csv")

"""Standardize the data"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_std = scaler.fit_transform(X_train)

x_test_std = scaler.transform(X_test)

"""Building the Neural Network"""

# importing tensorflow and Keras
import tensorflow as tf
tf.random.set_seed(3)
from tensorflow import keras

# Define the model
model = tf.keras.Sequential([
   tf.keras.layers.Flatten(input_shape=(30,)),       # Input layer with shape (30,)
    tf.keras.layers.Dense(20, activation='relu'),   # Hidden layer with 20 units and ReLU activation
    tf.keras.layers.Dense(2, activation='sigmoid')  # Output layer with 1 unit and sigmoid activation for binary classification
])

# compiling the Neural Network

model.compile(optimizer='adam',
              loss= 'sparse_categorical_crossentropy',
              metrics=['accuracy'])

#trainig the Neural Network

history = model.fit(X_train_std, Y_train, validation_split=0.1, epochs=10)

"""Visualizing accuracy and loss"""

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')

plt.legend(['training data', 'validation data'], loc = 'lower right')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')

plt.legend(['trainig data', 'validation data'],loc = 'upper right')

"""Accuracy of model on test data"""

loss, accuracy = model.evaluate(x_test_std, Y_test)
print(accuracy)

Y_pred = model.predict(x_test_std)

Y_pred

"""model.predict() gives the prediction probalility of each class for that data point"""

#   converting the prediction probability to class labels

Y_pred_labels = [np.argmax(i) for i in Y_pred]
print(Y_pred_labels)

"""Buliding the predictive system"""

input_data = (13.96,13.17,90.31,594.2,0.1248,0.09755,0.101,0.06615,0.1976,0.06457,0.5461,2.635,4.091,44.74,0.01004,0.03247,0.04763,0.02853,0.01715,0.005528,14.62,15.38,94.52,653.3,0.1394,0.1364,0.1559,0.1015,0.216,0.07253)

# change the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the numpy array as we are predicting for one data point
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

##standardizing the input dat
input_data_std = scaler.transform(input_data_reshaped)

prediction = model.predict(input_data_std)
print(prediction)

prediction_label = [np.argmax(prediction)]
print(prediction_label[0])

if(prediction_label[0] == 0):
 print('The Tumor is Malignant, person is Diagnosis with cancer')

else:
  print('The Tumor is Benign, no cancer cells detected')