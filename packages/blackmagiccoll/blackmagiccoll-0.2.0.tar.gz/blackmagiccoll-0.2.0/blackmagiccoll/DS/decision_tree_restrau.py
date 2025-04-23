import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt


data = {
    'Alt': ['Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'No', 'No'],
    'Bar': ['No', 'No', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'Yes', 'Yes'],
    'Fri': ['No', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'No'],
    'Hun': ['Yes', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'Yes'],
    'Pat': ['Some', 'Full', 'Some', 'Full', 'Full', 'Some', 'None', 'Some', 'Some', 'Full'],
    'Price': [1200, 2500, 2200, 1245, 4300, 3400, 1000, 3200, 3400, 3400],
    'Rain': ['No', 'No', 'No', 'No', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'No'],
    'Res': ['Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'No'],
    'Type': ['French', 'Thai', 'Burger', 'Thai', 'French', 'Italian', 'Burger', 'Thai', 'Thai', 'Burger'],
    'Est': ['0-10', '30-60', '0-10', '30-60', '>60', '0-10', '0-10', '0-10', '0-10', '>60'],
    'Wait': ['Yes', 'No', 'Yes', 'Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No']
}


df = pd.DataFrame(data)

le = LabelEncoder()
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = le.fit_transform(df[col])


X = df.drop('Wait', axis=1)
y = df['Wait']


model = DecisionTreeClassifier(criterion='entropy', random_state=42)
model.fit(X, y)

plt.figure(figsize=(12, 8))
tree.plot_tree(model, feature_names=X.columns, class_names=["No", "Yes"], filled=True)
plt.title("Decision Tree for Restaurant Waiting Problem")
plt.show()

tree_rules = export_text(model, feature_names=list(X.columns))
print(tree_rules)


new_data = pd.DataFrame({
    'Alt': [1],  # Yes
    'Bar': [0],  # No
    'Fri': [0],  # No
    'Hun': [1],  # Yes
    'Pat': [2],  # Full
    'Price': [2500],
    'Rain': [0],  # No
    'Res': [0],  # No
    'Type': [3],  # Thai
    'Est': [1]   # 30-60 mins
})

predicted_wait = model.predict(new_data)
print("Will the person wait?", "Yes" if predicted_wait[0] == 1 else "No")