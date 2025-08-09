from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>', course_detail, name='course'),
]
