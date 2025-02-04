from django.shortcuts import render , HttpResponse
from prediction.models import TopDisasters
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
    
    cities = TopDisasters.objects.order_by('s_number')

    return render (request, 'home.html',
                   {'cities': cities,}
                   )


def prediction(request):    
    return render(request, 'predictions.html')
