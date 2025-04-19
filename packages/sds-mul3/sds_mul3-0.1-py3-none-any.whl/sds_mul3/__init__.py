# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Step 1: Create the dataset
data = {
    'Bedrooms': [3, 3, 2, 4, 3, 4, 3, 3, 3, 3],
    'Bathrooms': [1, 2.25, 1, 3, 2, 4.5, 2.25, 1.5, 1, 2.5],
    'Sqft_living': [1180, 2570, 770, 1960, 1680, 5420, 1715, 1060, 1780, 1890],
    'Floors': [1, 2, 1, 1, 1, 1, 2, 1, 1, 2],
    'Grade': [7, 7, 6, 7, 8, 11, 7, 7, 7, 7],
    'Sqft_above': [1180, 2170, 770, 1050, 1680, 3890, 1715, 1060, 1050, 1890],
    'Sqft_basement': [0, 400, 0, 910, 0, 1530, 0, 0, 730, 0],
    'Price': [221900, 538000, 180000, 604000, 510000, 267800, 257500, 291850, 229500, 323000]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Step 2: Define features (X) and target (y)
X = df[['Bedrooms', 'Bathrooms', 'Sqft_living', 'Floors', 'Grade', 'Sqft_above', 'Sqft_basement']]
y = df['Price']

# Step 3: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 5: Make predictions on the test set
y_pred = model.predict(X_test)

# Step 6: Evaluate the model using regression metrics
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the results
print("Model Coefficients:")
for feature, coef in zip(X.columns, model.coef_):
    print(f"{feature}: {coef:.2f}")
print(f"\nIntercept: {model.intercept_:.2f}")
print("\nModel Performance Metrics:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"R² Score: {r2:.2f}")

# Optional: Predict a new house price (example)
# Define the new house as a DataFrame with the same column names
new_house = pd.DataFrame(
    [[3, 2.5, 2000, 2, 7, 1800, 200]],
    columns=['Bedrooms', 'Bathrooms', 'Sqft_living', 'Floors', 'Grade', 'Sqft_above', 'Sqft_basement']
)

# Make the prediction
predicted_price = model.predict(new_house)
print(f"\nPredicted Price for a new house: ${predicted_price[0]:.2f}")
