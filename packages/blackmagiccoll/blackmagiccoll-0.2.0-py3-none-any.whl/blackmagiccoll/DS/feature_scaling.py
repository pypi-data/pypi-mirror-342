import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

dataset = pd.read_excel("blackmagiccoll\\datasets\\Book2.xlsx")
df = pd.DataFrame(dataset)
print("OG Data: ", df)
num_cols = ['Mileage', 'Sell Price']


df_dummies = pd.get_dummies(df, columns=['Make', 'Model', 'Color'], drop_first=True)


scale = MinMaxScaler()
scaled_data =scale.fit_transform(df_dummies)
df_scaled = pd.DataFrame(scaled_data, columns=df_dummies.columns)
print("Scaled Data: ", df_scaled)


standard = StandardScaler()
standard_data = standard.fit_transform(df_dummies)
df_standard = pd.DataFrame(standard_data,columns=df_dummies.columns)
print(df_standard)
