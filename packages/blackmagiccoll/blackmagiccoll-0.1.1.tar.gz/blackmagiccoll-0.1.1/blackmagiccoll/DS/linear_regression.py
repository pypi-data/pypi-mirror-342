import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score


iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)


X = df[['petal width (cm)']]
y = df['petal length (cm)']

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

print("R² Score:", r2_score(y, y_pred))
print("Mean Squared Error:", mean_squared_error(y, y_pred))
print("Coefficient:", model.coef_[0])
print("Intercept:", model.intercept_)


plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Actual data')
plt.plot(X, y_pred, color='red', linewidth=2, label='Regression Line')
plt.xlabel("Petal Width (cm)")
plt.ylabel("Petal Length (cm)")
plt.title("Linear Regression on Iris Dataset")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
