from django.shortcuts import render , HttpResponse

# Create your views here.


def home(request):
    flood_data = [
    {
        'district': 'Gorakhpur',
        'flood_prone_areas': 'Villages along the Rapti and Ghaghra rivers.',
        'recent_incidents': 'In 2024, Gorakhpur faced severe flooding, affecting numerous villages and causing significant displacement.',
        'image': 'https://images.unsplash.com/photo-1604275689235-fdc521556c16?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
        'district': 'Ballia',
        'flood_prone_areas': 'Areas near the confluence of the Ganga and Ghaghra rivers.',
        'recent_incidents': 'In 2020, Ballia experienced flooding due to the Ganga river flowing above the danger mark, affecting several villages.'
    },
    {
        'district': 'Lakhimpur Kheri',
        'flood_prone_areas': 'Villages along the Sharda river.',
        'recent_incidents': 'In 2024, the Sharda river was reported to be flowing above the danger mark at Palia Kalan, leading to flooding in nearby areas.'
    },
    {
        'district': 'Bahraich',
        'flood_prone_areas': 'Regions near the Ghaghra river.',
        'recent_incidents': 'In 2024, Bahraich faced severe flooding, with water entering nearly two dozen villages situated near the Ghaghra river.'
    },
    {
        'district': 'Gonda',
        'flood_prone_areas': 'Villages along the Ghaghra river.',
        'recent_incidents': 'In 2024, Gonda experienced flooding, with water entering several villages near the Ghaghra river.'
    }
]
    return render(request, 'home.html', {'flood_data': flood_data})

def prediction(request):    
    return render(request, 'predictions.html')
