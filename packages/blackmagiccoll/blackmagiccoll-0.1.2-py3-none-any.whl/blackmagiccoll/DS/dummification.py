import pandas as pd

dataset = pd.read_excel('blackmagiccoll\\datasets\\DS\\Book1.xlsx')
dataset = dataset.dropna()

df = pd.DataFrame(dataset)
print("OG Data: ",df)

df_dummy = pd.get_dummies(df, drop_first=True)
print("Dummy Data: ",df_dummy)