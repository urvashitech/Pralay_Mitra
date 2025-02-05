from django.contrib import admin
from django.urls import path
from prediction import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),  # Home page
    path("predictions/", views.prediction, name="prediction"),  # Prediction page
    path('district/<str:district_name>/', views.district_detail, name='district_detail'), # District detail page
]
