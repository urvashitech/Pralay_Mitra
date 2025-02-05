import sqlite3
import requests
import time
from datetime import datetime
from pyproj import Proj, Transformer

# API KEYS
OPENWEATHER_API_KEY = "e655d3e9579db78790855c09dd3f3237"

# Define the WGS 84 coordinate system
wgs84 = Proj('epsg:4326')

# Define the UTM zone 44N coordinate system
utm_zone_44n = Proj('epsg:32644')

# Function to convert latitude and longitude to UTM coordinates
def latlon_to_utm(lat, lon):
    transformer = Transformer.from_proj(wgs84, utm_zone_44n)
    x, y = transformer.transform(lat, lon)
    return x, y

# Function to fetch elevation data from Open-Elevation API
def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0]["elevation"]
    else:
        print(f"Error fetching elevation for {lat}, {lon}")
        return None

# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {
            "Max_Temp": data["main"]["temp_max"],
            "Min_Temp": data["main"]["temp_min"],
            "Rainfall": data.get("rain", {}).get("1h", 0),  # Rain in last 1 hour
            "Relative_Humidity": data["main"]["humidity"],
            "Wind_Speed": data["wind"]["speed"],
            "Cloud_Coverage": data["clouds"]["all"]
        }
    else:
        print(f"Error fetching weather data: {data}")
        return None

# Function to fetch bright sunshine duration from NASA POWER API
def get_sunshine_duration(lat, lon):
    start_date = datetime.now().strftime('%Y%m%d')
    end_date = datetime.now().strftime('%Y%m%d')
    url = f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude={lon}&latitude={lat}&start={start_date}&end={end_date}&format=JSON"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return round(data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"][start_date] / 10, 2)  # Convert to hours
    else:
        print(f"Error fetching sunshine data: {data}")
        return None

# Connect to SQLite database
conn = sqlite3.connect('data/flood_data.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM flood_data')
conn.commit()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS flood_data (
    Sl INTEGER PRIMARY KEY,
    Station_Names TEXT,
    Year INTEGER,
    Month INTEGER,
    Max_Temp REAL,
    Min_Temp REAL,
    Rainfall REAL,
    Relative_Humidity REAL,
    Wind_Speed REAL,
    Cloud_Coverage REAL,
    Bright_Sunshine REAL,
    Station_Number INTEGER,
    X_COR REAL,
    Y_COR REAL,
    LATITUDE REAL,
    LONGITUDE REAL,
    ALT REAL,
    Period REAL,
    Flood INTEGER
)
''')

conn.commit()

# List of districts in Uttar Pradesh with latitude & longitude
districts = [
    {"name": "Agra", "lat": 27.1767, "lon": 78.0081, "pincode": 282001},
    {"name": "Aligarh", "lat": 27.8974, "lon": 78.0880, "pincode": 202001},
    {"name": "Allahabad", "lat": 25.4358, "lon": 81.8463, "pincode": 211001},
    {"name": "Ambedkar Nagar", "lat": 26.4411, "lon": 82.5361, "pincode": 224122},
    {"name": "Amethi", "lat": 26.1542, "lon": 81.8140, "pincode": 227405},
    {"name": "Amroha", "lat": 28.9031, "lon": 78.4698, "pincode": 244221},
    {"name": "Auraiya", "lat": 26.4633, "lon": 79.5117, "pincode": 206122},
    {"name": "Azamgarh", "lat": 26.0739, "lon": 83.1859, "pincode": 276001},
    {"name": "Baghpat", "lat": 28.9448, "lon": 77.2188, "pincode": 250609},
    {"name": "Bahraich", "lat": 27.5743, "lon": 81.5959, "pincode": 271801},
    {"name": "Ballia", "lat": 25.7586, "lon": 84.1480, "pincode": 277001},
    {"name": "Balrampur", "lat": 27.4277, "lon": 82.1873, "pincode": 271201},
    {"name": "Banda", "lat": 25.4753, "lon": 80.3358, "pincode": 210001},
    {"name": "Barabanki", "lat": 26.9393, "lon": 81.1836, "pincode": 225001},
    {"name": "Bareilly", "lat": 28.3670, "lon": 79.4304, "pincode": 243001},
    {"name": "Basti", "lat": 26.7945, "lon": 82.7329, "pincode": 272001},
    {"name": "Bhadohi", "lat": 25.3946, "lon": 82.5664, "pincode": 221401},
    {"name": "Bijnor", "lat": 29.3724, "lon": 78.1350, "pincode": 246701},
    {"name": "Budaun", "lat": 28.0362, "lon": 79.1267, "pincode": 243601},
    {"name": "Bulandshahr", "lat": 28.4030, "lon": 77.8573, "pincode": 203001},
    {"name": "Chandauli", "lat": 25.0810, "lon": 83.2670, "pincode": 232104},
    {"name": "Chitrakoot", "lat": 25.2016, "lon": 80.8322, "pincode": 210205},
    {"name": "Deoria", "lat": 26.5017, "lon": 83.7794, "pincode": 274001},
    {"name": "Etah", "lat": 27.5587, "lon": 78.6626, "pincode": 207001},
    {"name": "Etawah", "lat": 26.7855, "lon": 79.0155, "pincode": 206001},
    {"name": "Faizabad", "lat": 26.7755, "lon": 82.1502, "pincode": 224001},
    {"name": "Farrukhabad", "lat": 27.3905, "lon": 79.5801, "pincode": 209625},
    {"name": "Fatehpur", "lat": 25.9304, "lon": 80.8136, "pincode": 212601},
    {"name": "Firozabad", "lat": 27.1591, "lon": 78.3958, "pincode": 283203},
    {"name": "Gautam Buddha Nagar", "lat": 28.5355, "lon": 77.3910, "pincode": 201301},
    {"name": "Ghaziabad", "lat": 28.6692, "lon": 77.4538, "pincode": 201001},
    {"name": "Ghazipur", "lat": 25.5805, "lon": 83.5806, "pincode": 233001},
    {"name": "Gonda", "lat": 27.1325, "lon": 81.9690, "pincode": 271001},
    {"name": "Gorakhpur", "lat": 26.7606, "lon": 83.3732, "pincode": 273001},
    {"name": "Hamirpur", "lat": 25.9560, "lon": 80.1484, "pincode": 210301},
    {"name": "Hapur", "lat": 28.7306, "lon": 77.7754, "pincode": 245101},
    {"name": "Hardoi", "lat": 27.3943, "lon": 80.1311, "pincode": 241001},
    {"name": "Hathras", "lat": 27.5969, "lon": 78.0524, "pincode": 204101},
    {"name": "Jalaun", "lat": 26.1451, "lon": 79.3366, "pincode": 285123},
    {"name": "Jaunpur", "lat": 25.7463, "lon": 82.6836, "pincode": 222001},
    {"name": "Jhansi", "lat": 25.4484, "lon": 78.5685, "pincode": 284001},
    {"name": "Kannauj", "lat": 27.0553, "lon": 79.9182, "pincode": 209725},
    {"name": "Kanpur Dehat", "lat": 26.4294, "lon": 79.9634, "pincode": 209101},
    {"name": "Kanpur Nagar", "lat": 26.4499, "lon": 80.3319, "pincode": 208001},
    {"name": "Kasganj", "lat": 27.8054, "lon": 78.6460, "pincode": 207123},
    {"name": "Kaushambi", "lat": 25.5302, "lon": 81.3784, "pincode": 212201},
    {"name": "Kushinagar", "lat": 26.7397, "lon": 83.8887, "pincode": 274403},
    {"name": "Lakhimpur Kheri", "lat": 27.8974, "lon": 80.7974, "pincode": 262701},
    {"name": "Lalitpur", "lat": 24.6901, "lon": 78.4189, "pincode": 284403},
    {"name": "Lucknow", "lat": 26.8467, "lon": 80.9462, "pincode": 226001},
    {"name": "Maharajganj", "lat": 27.1170, "lon": 83.5656, "pincode": 273303},
    {"name": "Mahoba", "lat": 25.2926, "lon": 79.8723, "pincode": 210427},
    {"name": "Mainpuri", "lat": 27.2253, "lon": 79.0288, "pincode": 205001},
    {"name": "Mathura", "lat": 27.4924, "lon": 77.6737, "pincode": 281001},
    {"name": "Mau", "lat": 25.9417, "lon": 83.5611, "pincode": 275101},
    {"name": "Meerut", "lat": 28.9845, "lon": 77.7064, "pincode": 250001},
    {"name": "Mirzapur", "lat": 25.1440, "lon": 82.5653, "pincode": 231001},
    {"name": "Moradabad", "lat": 28.8386, "lon": 78.7733, "pincode": 244001},
    {"name": "Muzaffarnagar", "lat": 29.4739, "lon": 77.7041, "pincode": 251001},
    {"name": "Pilibhit", "lat": 28.6312, "lon": 79.8047, "pincode": 262001},
    {"name": "Pratapgarh", "lat": 25.8605, "lon": 81.9800, "pincode": 230001},
    {"name": "Raebareli", "lat": 26.2303, "lon": 81.2404, "pincode": 229001},
    {"name": "Rampur", "lat": 28.7895, "lon": 79.0250, "pincode": 244901},
    {"name": "Saharanpur", "lat": 29.9640, "lon": 77.5460, "pincode": 247001},
    {"name": "Sambhal", "lat": 28.5849, "lon": 78.5661, "pincode": 244302},
    {"name": "Sant Kabir Nagar", "lat": 26.7895, "lon": 83.0666, "pincode": 272175},
    {"name": "Shahjahanpur", "lat": 27.8815, "lon": 79.9090, "pincode": 242001},
    {"name": "Shamli", "lat": 29.4493, "lon": 77.3092, "pincode": 247776},
    {"name": "Shravasti", "lat": 27.5077, "lon": 82.0485, "pincode": 271805},
    {"name": "Siddharthnagar", "lat": 27.2742, "lon": 83.0784, "pincode": 272207},
    {"name": "Sitapur", "lat": 27.5706, "lon": 80.6828, "pincode": 261001},
    {"name": "Sonbhadra", "lat": 24.6869, "lon": 83.0666, "pincode": 231213},
    {"name": "Sultanpur", "lat": 26.2648, "lon": 82.0727, "pincode": 228001},
    {"name": "Unnao", "lat": 26.5471, "lon": 80.4878, "pincode": 209801},
    {"name": "Varanasi", "lat": 25.3176, "lon": 82.9739, "pincode": 221001}
]

# Get current year and month
curr_year = datetime.now().year
curr_month = datetime.now().month

# Insert data into the database
for i, district in enumerate(districts, start=1):
    print(f"Fetching data for {district['name']}...")

    weather = get_weather_data(district["lat"], district["lon"])
    sunshine = get_sunshine_duration(district["lat"], district["lon"])
    elevation = get_elevation(district["lat"], district["lon"])
    x_cor, y_cor = latlon_to_utm(district["lat"], district["lon"])

    if weather:
        cursor.execute('''
        INSERT INTO flood_data (Station_Names, Year, Month, Max_Temp, Min_Temp, Rainfall, Relative_Humidity, Wind_Speed, Cloud_Coverage, Bright_Sunshine, Station_Number, X_COR, Y_COR, LATITUDE, LONGITUDE, ALT, Period, Flood)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (district["name"], curr_year, curr_month, weather["Max_Temp"], weather["Min_Temp"], weather["Rainfall"], weather["Relative_Humidity"], weather["Wind_Speed"], weather["Cloud_Coverage"], sunshine, district["pincode"], x_cor, y_cor, district["lat"], district["lon"], elevation, float(f"{curr_year}.{curr_month}"), None))

    time.sleep(1)  # Avoid hitting API rate limits

conn.commit()
conn.close()