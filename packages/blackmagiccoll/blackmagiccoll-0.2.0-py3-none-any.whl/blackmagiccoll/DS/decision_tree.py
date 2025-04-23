import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_excel("blackmagiccoll\\datasets\\Book3.xlsx")
df = pd.DataFrame(data)
print("OG Data: ", df.head())

le = LabelEncoder()
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = le.fit_transform(df[col])
df.drop('Date',axis=1,inplace=True)
X = df.drop('Playtennis', axis=1)
y = df['Playtennis']

model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=42)
model.fit(X, y)

plt.figure(figsize=(12, 8))
tree.plot_tree(model, feature_names=X.columns, class_names=['No', 'Yes'], filled=True)
plt.title("Decision Tree Visualization")
plt.show()

tree_rules = export_text(model, feature_names=list(X.columns))
print(tree_rules)

new_data = pd.DataFrame({
    'Outlook': [0],
    'Wind': [1],  
})

prediction = model.predict(new_data)
print("Will the person play?", "Yes" if prediction[0] == 1 else "No")