
from django.urls import path

from . import views

urlpatterns = [
    # route jest doklejane do urlstring głównego urls.py
    path('', views.index, name='index'),
    path('<int:id>', views.detail, name='detail'),
]
