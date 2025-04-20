import pandas as pd
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt


data = {
    'Height': [151, 174, 138, 186, 128, 136, 179, 163, 152],
    'Weight': [63, 81, 56, 91, 47, 57, 76, 72, 62]
}

df = pd.DataFrame(data)

X = df[['Height']]
y = df['Weight']

model = DecisionTreeRegressor(random_state=42)
model.fit(X, y)

plt.figure(figsize=(12, 8))
plot_tree(model, feature_names=['Height'], filled=True, rounded=True)
plt.title("Decision Tree Model for Predicting Weight Based on Height")
plt.show()

new_height = [[160]]  # Example: height 160
predicted_weight = model.predict(new_height)
print(f"Predicted Weight for height {new_height[0][0]} is {predicted_weight[0]:.2f}")