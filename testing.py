import pandas as pd
import numpy as np
import pickle

# Importing the dataset
df = pd.read_csv('new_normalized.csv')
print(df.head())

X = df.iloc[:, :5].values
y = df.iloc[:, 7].values

print(X)
print(y)

# Splitting the dataset into Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 206)
X_train = X_train.T
y_train = y_train.reshape(1, X_train.shape[1])
X_test = X_test.T
y_test = y_test.reshape(1, X_test.shape[1])
print(np.shape(X_train), np.shape(X_test), np.shape(y_train), np.shape(y_test))

with open('test1', 'rb') as f:
    model = pickle.load(f)

pred = model.predict(X_test[:, 1])
print(pred)
print(y_test[:, 1])