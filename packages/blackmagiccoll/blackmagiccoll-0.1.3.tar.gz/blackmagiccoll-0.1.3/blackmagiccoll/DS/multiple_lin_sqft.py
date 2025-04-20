import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Creating the dataset
data = {
    "Bedrooms": [3, 3, 2, 3, 2, 4, 3, 3, 3, 3],
    "Bathrooms": [1, 2.25, 1, 1, 1, 4.5, 2.25, 1.5, 1, 2.5],
    "Sqft_living": [1180, 2570, 770, 1960, 1680, 5420, 1715, 1060, 1780, 1890],
    "Floors": [1, 2, 1, 1, 1, 1, 2, 1, 1, 2],
    "Grade": [7, 7, 6, 7, 7, 11, 7, 7, 7, 8],
    "Sqft_above": [1180, 2170, 770, 1050, 1680, 3890, 1715, 1060, 1050, 1860],
    "Sqft_basement": [0, 400, 0, 910, 0, 1530, 0, 0, 730, 1700],
    "Price": [221900, 538000, 180000, 604000, 510000, 267800, 257500, 291850, 229500, 662500]
}

df = pd.DataFrame(data)

X = df.drop(columns=["Price"])
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Model Evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")
print(f"R² Score: {r2}")

plt.figure(figsize=(6, 4))
plt.scatter(df["Sqft_living"], df["Price"], color="blue", alpha=0.5)
plt.xlabel("Sqft Living Area")
plt.ylabel("House Price")
plt.title("Sqft Living vs. Price")
plt.show()

plt.figure(figsize=(6, 4))
plt.scatter(y_test, y_pred, color="red", alpha=0.5)
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.title("Predicted vs. Actual House Prices")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color="black", linestyle="dashed")
plt.show()
