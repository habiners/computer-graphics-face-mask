import numpy as np

class LogisticRegression:
    
    def __init__(self, lr=0.001, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = None
        
    def fit(self, X, y):
        rows, cols = np.shape(X.T)
        self.weights = np.zeros((cols, 1))
        self.bias = 0
        
        cost_list = []
        
        for i in range(self.epochs):
            linearModel = np.dot(self.weights.T, X) + self.bias
            y_predicted = self._sigmoid(linearModel)
            
            # Cost Function
            cost = -(1 / rows) * np.sum(y * np.log(y_predicted) + (1-y) * np.log(1-y_predicted))
            
            # Gradient descent
            dw = (1 / rows) * np.dot(y_predicted - y, X.T)
            db = (1 / rows) * np.sum(y_predicted - y)
            
            # Update values for the next epoch
            self.weights -= self.lr * dw.T
            self.bias -= self.lr * db
            
            # Show error progress
            cost_list.append(cost)
            if (i % (self.epochs/10) == 0):
                print("Cost after", i, "iteration is: ", cost)
            
            
    def predict(self, X):
        linearModel = np.dot(self.weights.T, X) + self.bias
        y_predicted = self._sigmoid(linearModel)
        y_predicted = y_predicted > 0.5
        y_predicted = np.array(y_predicted, dtype = 'int64')
        # y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
        return y_predicted
    
    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))