import subprocess
import sqlite3
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder

class CustomLabelEncoder(LabelEncoder):
    def fit(self, y):
        super().fit(y)
        self.classes_ = np.append(self.classes_, 'unknown')
        return self

    def transform(self, y):
        unknown_label = len(self.classes_) - 1
        y = np.array([x if x in self.classes_ else 'unknown' for x in y])
        return super().transform(y)

    def fit_transform(self, y):
        return self.fit(y).transform(y)

# Step 1: Run the data_fetcher script
subprocess.run(["python3", "scripts/data_fetcher.py"])

# Step 2: Connect to SQLite database
conn = sqlite3.connect('prediction/ml/data/flood_data.db')
cursor = conn.cursor()

# Step 3: Fetch new data from the database
cursor.execute('''
SELECT Sl, Station_Names, Year, Month, Max_Temp, Min_Temp, Rainfall, Relative_Humidity, Wind_Speed, Cloud_Coverage, Bright_Sunshine, Station_Number, X_COR, Y_COR, LATITUDE, LONGITUDE, ALT, Period
FROM flood_data
WHERE Flood IS NULL
''')
rows = cursor.fetchall()

# Step 4: Convert to DataFrame
columns = ['Sl', 'Station_Names', 'Year', 'Month', 'Max_Temp', 'Min_Temp', 'Rainfall', 'Relative_Humidity', 'Wind_Speed', 'Cloud_Coverage', 'Bright_Sunshine', 'Station_Number', 'X_COR', 'Y_COR', 'LATITUDE', 'LONGITUDE', 'ALT', 'Period']
operational_data = pd.DataFrame(rows, columns=columns)

# Step 5: Handle missing values
operational_data.fillna({col: operational_data[col].mode()[0] for col in operational_data.columns}, inplace=True)

# Step 6: Initialize the custom label encoder
label_encoder = CustomLabelEncoder()
operational_data['Station_Names'] = label_encoder.fit_transform(operational_data['Station_Names'])

# Encode categorical variables
operational_data['Station_Names'] = label_encoder.transform(operational_data['Station_Names'])

# Step 7: Load the model
model = joblib.load('prediction/ml/models/flood_prediction_model.pkl')

# Make predictions
predictions = model.predict(operational_data)

# Add predictions to the operational data
operational_data['Flood'] = predictions

# Save predictions back to the database
for index, row in operational_data.iterrows():
    cursor.execute('''
        UPDATE flood_data
        SET Flood = ?
        WHERE Sl = ?
    ''', (row['Flood'], row['Sl']))

# Commit the changes and close the connection
conn.commit()
conn.close()

subprocess.run(["python3", "scripts/severity_calculator.py"])

print("Pipeline executed successfully.")