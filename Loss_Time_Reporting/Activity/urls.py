from django.urls import path
from Activity.views import *

app_name = 'Activity'

urlpatterns = [
    path('', Activity_List, name='Activity_List'),
]
