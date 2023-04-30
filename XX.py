import numpy as np
from sklearn.linear_model import LinearRegression

# Define the input data (house sizes) and target data (prices)
X = np.array([[500], [1200], [1400], [1600], [1800], [2000], [2200], [2400], [2600], [2800]])
y = np.array([150000, 170000, 190000, 210000, 230000, 250000, 270000, 290000, 310000, 330000])

# Create a linear regression model and fit the data
model = LinearRegression()
model.fit(X, y)

# Predict the price of a house with a size of 3000 square feet
s=6000
house_size = np.array([[s]])
predicted_price = model.predict(house_size)

print(f"The predicted price of a house with a size of {s} square feet is ${predicted_price[0]:,.2f}.")
