
import imp
from random import seed
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # route jest doklejane do urlstring głównego urls.py
    path('', views.index, name='index'),
    path('create-trade', views.create_trade, name='create-trade'),
    path('update-trade/<str:pk>', views.update_trade, name='update-trade')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
