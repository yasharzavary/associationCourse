from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>', sign, name='sign'),
    path('siteAdmin/OSE', send_emails_offline, name='offlineSendEmails'),
]