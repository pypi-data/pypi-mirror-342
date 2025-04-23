from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd

boston = fetch_openml(name="boston", version=1, as_frame=True)
df = boston.data

standard_scaler = StandardScaler()
standardized_data = standard_scaler.fit_transform(df)
standardized_df = pd.DataFrame(standardized_data, columns=df.columns)

minmax_scaler = MinMaxScaler()
normalized_data = minmax_scaler.fit_transform(df)
normalized_df = pd.DataFrame(normalized_data, columns=df.columns)

print("Standardized Data (first 5 rows):")
print(standardized_df.head())

print("\nNormalized Data (first 5 rows):")
print(normalized_df.head())
