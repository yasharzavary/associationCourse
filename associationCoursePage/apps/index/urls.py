from django.urls import path, URLPattern
from .views import *

urlpatterns = [
    path('', index, name='index'),

]