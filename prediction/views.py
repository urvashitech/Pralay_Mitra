from django.shortcuts import render , HttpResponse
from prediction.models import TopDisasters
import sqlite3
# Create your views here.


def home(request):
    flood_data = [
    {
        'district': 'Gorakhpur',
        'flood_prone_areas': 'Villages along the Rapti and Ghaghra rivers.',
        'recent_incidents': 'In 2024, Gorakhpur faced severe flooding, affecting numerous villages and causing significant displacement.',
        'image': 'images/img1.jpg'
    },
    {
        'district': 'Ballia',
        'flood_prone_areas': 'Areas near the confluence of the Ganga and Ghaghra rivers.',
        'recent_incidents': 'In 2020, Ballia experienced flooding due to the Ganga river flowing above the danger mark, affecting several villages.',
        'image': 'images/ballai.jpg'
    },
    {
        'district': 'Lakhimpur Kheri',
        'flood_prone_areas': 'Villages along the Sharda river.',
        'recent_incidents': 'In 2024, the Sharda river was reported to be flowing above the danger mark at Palia Kalan, leading to flooding in nearby areas.',
        'image': 'images/lakhimpur.webp'
    },
    {
        'district': 'Bahraich',
        'flood_prone_areas': 'Regions near the Ghaghra river.',
        'recent_incidents': 'In 2024, Bahraich faced severe flooding, with water entering nearly two dozen villages situated near the Ghaghra river.',
        'image': 'images/bahraich.avif'
    },
    {
        'district': 'Gonda',
        'flood_prone_areas': 'Villages along the Ghaghra river.',
        'recent_incidents': 'In 2024, Gonda experienced flooding, with water entering several villages near the Ghaghra river.',
        'image': 'images/gonda.jpg'
    }
]
    
    cities = TopDisasters.objects.order_by('rainFall')

    return render (request, 'home.html',
                   {'cities': cities,}
                   )


def prediction(request):   
    district_name = [
        'Aligarh','Ambedkar Nagar','Amethi','Amroha','Auraiya','Azamgarh','Baghpat','Bahraich','Ballia','Balrampur','Banda','Barabanki','Bareilly','Basti','Bhadohi','Bijnor','Budaun','Bulandshahr','Chandauli','Chitrakoot','Deoria','Etah','Etawah','Farrukhabad','Fatehpur','Firozabad','Gautam Buddha Nagar','Ghaziabad','Ghazipur','Gonda','Hamirpur','Hapur','Hardoi','Hathras','Jalaun','Jaunpur','Kannauj','Kanpur Dehat','Kanpur Nagar','Kasganj','Kaushambi','Kushinagar','Lakhimpur Kheri','Lalitpur','Maharajganj','Mahoba','Mainpuri','Mau','Meerut','Mirzapur','Moradabad','Muzaffarnagar','Pilibhit','Pratapgarh','Prayagraj','Raebareli','Rampur','Saharanpur','Sambhal','Sant Kabir Nagar','Shahjahanpur','Shamli','Shrawasti','Siddharthnagar','Sitapur','Sonbhadra','Sultanpur','Unnao',
        ] 
    return render(request, 'predictions.html', {'district_name': district_name})

def district_detail(request, district_name):
    # Path to your database file
    db_path = "prediction/ml/data/flood_data.db"

     # Connecting to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

     # Fetch district data
    query = "SELECT  Max_Temp ,Rainfall, Wind_Speed FROM flood_data WHERE Station_Names = ?"
    cursor.execute(query, (district_name,))
    result = cursor.fetchone()

    if result:
        temperature , rainfall, wind_speed = result
    else:
        rainfall = wind_speed = None  # Handle case when no data is found 
    # Close the connection
    conn.close()
    return render(request, 'district_detail.html', {"district": district_name,
        "temperature": temperature,
        "rainfall": rainfall,
        "windspeed": wind_speed,})
