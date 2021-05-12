import pandas as pd
import numpy as np

# Importing the dataset
df = pd.read_csv('new_normalized.csv')
print(df.head())

X = df.iloc[:, :5].values
y = df.iloc[:, 7].values

print(X)
print(y)

# Splitting the dataset into Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 127)
X_train = X_train.T
y_train = y_train.reshape(1, X_train.shape[1])
X_test = X_test.T
y_test = y_test.reshape(1, X_test.shape[1])
print(np.shape(X_train), np.shape(X_test), np.shape(y_train), np.shape(y_test))


from logistic_regression import LogisticRegression
model = LogisticRegression(lr=0.0001, epochs=1000)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

def accuracy(y_true, y_pred):
    # accuracy = np.sum(y_true == y_pred) / len(y_true)
    accuracy = (1 - np.sum(np.abs(y_pred - y_true)) / y_true.shape[1]) * 100
    return accuracy

print("Accuracy: ", accuracy(y_test, predictions))

print(y_test)
print(predictions)




# def sigmoid(z):
# 	return 1/(1 + np.exp(-z))


# def cost_function(x, y, theta):
# 	h = sigmoid(x@theta)
# 	print(np.log(h).shape)
# 	one = np.ones((y.shape[0],1))
# 	return (-((y.T@np.log(h)) + (one-y).T@np.log(one - h))/(y.shape[0]))

# def gradient_descent(x, y, theta, learning_rate=0.1, num_epochs=10):
# 	m = x.shape[0]
# 	J_all = []
	
# 	for _ in range(num_epochs):
# 		h_x = sigmoid(x@theta)
# 		cost_ = (1/m)*(x.T@(h_x - y))
# 		theta = theta - (learning_rate)*cost_
# 		J_all.append(cost_function(x, y, theta))

# 	return theta, J_all 


# Wa pako kasabot ani tanan

# x, y = load_data("student_result_data.txt")
# y = np.reshape(y, (y.shape[0], 1))
# x = np.hstack((np.ones((x.shape[0], 1)), x))
# theta = np.zeros((x.shape[1], 1))
# learning_rate = 0.001
# num_epochs = 100
# theta, J_all = gradient_descent(x, y, theta, learning_rate, num_epochs)
# J = cost_function(x, y, theta)
# print(theta)
# print(J)

# n_epochs = []
# jplot = []
# count = 0
# for i in J_all:
# 	jplot.append(i[0][0])
# 	n_epochs.append(count)
# 	count += 1
# jplot = np.array(jplot)
# n_epochs = np.array(n_epochs)
# plot_cost(jplot, n_epochs)

# test(theta, [1, 48, 85])
