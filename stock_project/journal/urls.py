
from django.urls import path

from . import views

urlpatterns = [
    # route jest doklejane do urlstring głównego urls.py
    path('', views.index, name='index'),
    path('create-trade', views.create_trade, name='create-trade'),
    path('update-trade/<int:pk>', views.update_trade, name='update-trade')
]
