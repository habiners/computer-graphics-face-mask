import pandas as pd
import numpy as np

df = pd.read_csv('new_normalized.csv')
print(df.head(10))

def sigmoid(z):
	return 1/(1 + np.exp(-z))
