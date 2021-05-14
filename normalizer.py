from sklearn import preprocessing
import pandas as pd

first_csv = pd.read_csv("results.csv")
scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1))
names = first_csv.columns
d = scaler.fit_transform(first_csv)
scaled_df = pd.DataFrame(d, columns=names)
scaled_df.head()
scaled_df.to_csv(r'normalized.csv', index = False)