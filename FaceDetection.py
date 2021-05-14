import pandas as pd
import numpy as np
import pickle

# Importing the dataset
df = pd.read_csv('new_results.csv')
print(df.head())

X = df.iloc[:, :5].values
y = df.iloc[:, 8].values

print(X)
print(y)

# Splitting the dataset into Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 26)
X_train = X_train.T
y_train = y_train.reshape(1, X_train.shape[1])
X_test = X_test.T
y_test = y_test.reshape(1, X_test.shape[1])
print(np.shape(X_train), np.shape(X_test), np.shape(y_train), np.shape(y_test))


from logistic_regression import LogisticRegression
model = LogisticRegression(lr=0.1, epochs=20000)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

def accuracy(y_true, y_pred):
    # accuracy = np.sum(y_true == y_pred) / len(y_true)
    accuracy = (1 - np.sum(np.abs(y_pred - y_true)) / y_true.shape[1]) * 100
    return accuracy

print("Accuracy: ", accuracy(y_test, predictions))

print(y_test)
print(predictions)

testing = model.predict(X_test[:, 1])
print(testing)
print(y_test[:, 1])