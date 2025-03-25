import pandas as pd
import numpy as np

# Set a seed for reproducibility
np.random.seed(42)

# Define number of rows
n_rows = 10000

# Generate dummy data
data = {
    "longitude": np.random.uniform(-124.35, -114.31, n_rows),
    "latitude": np.random.uniform(32.54, 42.01, n_rows),
    "housing_median_age": np.random.randint(1, 60, n_rows),
    "total_rooms": np.random.randint(50, 10000, n_rows),
    "total_bedrooms": np.random.randint(10, 2000, n_rows),
    "population": np.random.randint(100, 5000, n_rows),
    "households": np.random.randint(50, 2000, n_rows),
    "median_income": np.random.uniform(0.5, 15, n_rows),
    "ocean_proximity": np.random.choice(["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"], n_rows)
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to an Excel file
df.to_excel("dummy_data.xlsx", index=False)
print("dummy_data.xlsx has been created with", n_rows, "rows.")
