from django.shortcuts import render , HttpResponse
from prediction.models import TopDisasters, Bulletin
import sqlite3
import folium
# Create your views here.


def home(request):
    
    bulletins = Bulletin.objects.order_by('-date')[:5]
    cities = TopDisasters.objects.order_by('rainFall')
    db_path = "prediction/ml/data/flood_data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch district data including latitude, longitude, and severity score
    query = "SELECT Station_Names, Latitude, Longitude, Severity_Percentage FROM flood_data "
    cursor.execute(query)
    districts_data = cursor.fetchall()
    
    # Close the connection to the database
    conn.close()

    # Create a folium map centered on Uttar Pradesh
    m = folium.Map(location=[26.8, 80.9], zoom_start=6)  # Coordinates for UP
    
    # Function to assign color based on severity score
    def get_color(severity):
        if severity <= 25:
            return 'lightgreen'
        elif severity <= 50:
            return 'yellow'
        elif severity <= 75:
            return 'orange'
        else:
            return 'red'
    
    # Add markers for each district with dynamic severity color coding
    for district in districts_data:
        district_name, latitude, longitude, severity_score = district
        color = get_color(severity_score)
        
        # Add each district as a circle marker
        folium.CircleMarker(
            location=[latitude, longitude],
            radius=8,
            color='black',
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"<strong>{district_name}</strong><br>Severity: {severity_score}%"
        ).add_to(m)
    
    # Save the map as HTML
    map_html = m._repr_html_()

    return render (request, 'home.html',
                   {'cities': cities, 'map_html': map_html, 'bulletins': bulletins}
                   )


def prediction(request):   
    district_name = [
        'Aligarh','Ambedkar Nagar','Amethi','Amroha','Auraiya','Azamgarh','Baghpat','Bahraich','Ballia','Balrampur','Banda','Barabanki','Bareilly','Basti','Bhadohi','Bijnor','Budaun','Bulandshahr','Chandauli','Chitrakoot','Deoria','Etah','Etawah','Farrukhabad','Fatehpur','Firozabad','Gautam Buddha Nagar','Ghaziabad','Ghazipur','Gonda','Hamirpur','Hapur','Hardoi','Hathras','Jalaun','Jaunpur','Kannauj','Kanpur Dehat','Kanpur Nagar','Kasganj','Kaushambi','Kushinagar','Lakhimpur Kheri','Lalitpur','Maharajganj','Mahoba','Mainpuri','Mau','Meerut','Mirzapur','Moradabad','Muzaffarnagar','Pilibhit','Pratapgarh','Prayagraj','Raebareli','Rampur','Saharanpur','Sambhal','Sant Kabir Nagar','Shahjahanpur','Shamli','Shrawasti','Siddharthnagar','Sitapur','Sonbhadra','Sultanpur','Unnao',
        ] 
    return render(request, 'predictions.html', {'district_name': district_name})

def district_detail(request, district_name):
    district_name = district_name.replace('-', ' ').strip().capitalize()
    # Path to your database file
    db_path = "prediction/ml/data/flood_data.db"

     # Connecting to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

     # Fetch district data
    query = "SELECT  Station_Names, Period, Station_Number, Max_Temp, Rainfall, Relative_Humidity, Wind_Speed, Cloud_Coverage, Flood, Severity_Percentage   FROM flood_data WHERE Station_Names = ?"
    cursor.execute(query, (district_name,))
    result = cursor.fetchone()

    if result:
      (Station_Names, Period,Station_Number, Max_Temp, Rainfall, Relative_Humidity, Wind_Speed, Cloud_Coverage,Flood, Severity_Percentage) = result
    else:
       Station_Names= Period = Station_Number = Max_Temp = Rainfall = Relative_Humidity = Wind_Speed = Cloud_Coverage = Flood = Severity_Percentage =  None  # Handle case when no data is found 
    # Close the connection
    conn.close()

    card = [
        {"title": "Period", "value": f"{Period}", "icon": "fa-calendar-days","color": "#B0C4DE "},
         {"title": "Pin Code", "value": f"{Station_Number}", "icon": "fa-map-pin","color":"#FF4500"},
        {"title": "Temperature", "value": f"{Max_Temp} °C", "icon": "fa-temperature-high","color": "#FF5733"},
        {"title": "Rainfall", "value": f"{Rainfall} mm", "icon": "fa-cloud-rain","color": "#4682B4"},
        {"title": "Humidity", "value": f"{Relative_Humidity}%", "icon": "fa-tint", "color": "#1E90FF"},
        {"title": "Wind Speed", "value": f"{Wind_Speed} km/h", "icon": "fa-wind","color": "#A9A9A9"},
        {"title": "Cloud Coverage", "value": f"{Cloud_Coverage}%", "icon": "fa-cloud","color": "#B0C4DE"},
        {"title": "Severity Percentage", "value": f"{Severity_Percentage}%", "icon": "fa-exclamation-triangle","color": "#FF4500"},
        {"title": "Flood", "value": f"{Flood}", "icon": "fa-exclamation-triangle", "color": "#FFD700"},]
    
    return render(request, 'district_detail.html', {"district": district_name,
                                                    "station_name": Station_Names,
                                                    "card": card,
        })
def response(request):
    return render(request, 'response.html')

def resource(request):
    return render(request, 'resource.html')