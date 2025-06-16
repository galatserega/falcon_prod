from django.urls import path
from . import views

app_name = 'catalog'  

urlpatterns = [
    path('download/', views.download_catalog, name='download_catalog'),
]
