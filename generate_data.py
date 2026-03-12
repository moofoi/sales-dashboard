import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard']
regions = ['North', 'South', 'East', 'West']
months = pd.date_range(start='2024-01-01', periods=n, freq='D')

data = {
    'date': months,
    'product': np.random.choice(products, n),
    'region': np.random.choice(regions, n),
    'units_sold': np.random.randint(1, 50, n),
    'price': np.random.uniform(100, 2000, n).round(2),
}

df = pd.DataFrame(data)
df['revenue'] = (df['units_sold'] * df['price']).round(2)
df.to_csv('sales_data.csv', index=False)
print("Sales data created!")