import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler

# Connect to the SQLite database
db_path = 'prediction/ml/data/flood_data.db'
conn = sqlite3.connect(db_path)

# Load the data from the database
query = "SELECT * FROM flood_data"
data = pd.read_sql_query(query, conn)

# Select relevant features
features = ['Rainfall', 'Relative_Humidity', 'Wind_Speed']

# Normalize the features
scaler = MinMaxScaler()
data[features] = scaler.fit_transform(data[features])

# Assign weights to each feature
weights = {
    'Rainfall': 0.5,
    'Relative_Humidity': 0.3,
    'Wind_Speed': 0.2
}

# Calculate the severity score
data['Severity_Score'] = (
    data['Rainfall'] * weights['Rainfall'] +
    data['Relative_Humidity'] * weights['Relative_Humidity'] +
    data['Wind_Speed'] * weights['Wind_Speed']
)

# Convert severity score to percentage
data['Severity_Percentage'] = data['Severity_Score'] * 100

# Write the updated data back to the database
data.to_sql('flood_data', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print("Severity scores calculated and saved to the database")