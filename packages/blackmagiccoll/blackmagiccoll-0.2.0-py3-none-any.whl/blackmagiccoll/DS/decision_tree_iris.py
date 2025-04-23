from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
import matplotlib.pyplot as plt

iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names

model = DecisionTreeClassifier(criterion='entropy', random_state=42)
model.fit(X, y)

rules = export_text(model, feature_names=feature_names)
print("=== Decision Tree Rules ===")
print(rules)

plt.figure(figsize=(12, 8))
plot_tree(model, feature_names=feature_names, class_names=target_names, filled=True)
plt.title("Decision Tree Visualization for Iris Dataset")
plt.show()
