from django.shortcuts import render , HttpResponse
from prediction.models import TopDisasters
import sqlite3

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot_service import get_chat_response
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
    # Example data for the response plan
    safety_tips = {
        "before": [
            "Prepare an emergency kit with essential supplies.",
            "Create a family emergency plan and practice it regularly.",
            "Stay informed about potential hazards in your area.",
        ],
        "during": [
            "Follow evacuation orders from local authorities.",
            "Stay indoors and away from windows during severe weather.",
            "Use battery-powered devices to stay informed if power is lost.",
        ],
        "after": [
            "Avoid floodwaters and downed power lines.",
            "Check for injuries and provide first aid if needed.",
            "Contact emergency services for assistance if required.",
        ],
    }

    return render(request, 'response.html', {
        "safety_tips": safety_tips,
    })

def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phase = data.get("phase", "before")
            user_message = data.get("message", "")
            bot_response = get_chat_response(phase, user_message)
            return JsonResponse({"response": bot_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)

def resource(request):
    return render(request, 'resource.html')