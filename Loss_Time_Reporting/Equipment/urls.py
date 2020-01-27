from django.contrib import admin
from django.urls import path
from Equipment.views import *

app_name = 'Equipment'

urlpatterns = [
    path('', Equipment_List, name='Equipment_List'),
    path('create/', Equipment_Create, name='Equipment_Create'),
    path('detail/<str:equipment_id>/', Equipment_Detail, name='Equipment_Detail'),
    path('edit/<str:equipment_id>/', Equipment_Edit, name='Equipment_Edit'),
    path('delete/<str:equipment_id>/', Equipment_Delete, name='Equipment_Delete'),

    # URL for Location Equippmet
    path('locate_list', Locate_List, name='Locate_List'),
    path('locate_create/', Locate_Create, name='Locate_Create'),
    path('locate_detail/<str:locate_id>/', Locate_Detail, name='Locate_Detail'),
    path('locate_edit/<str:locate_id>/', Locate_Edit, name='Locate_Edit'),
    path('locate_delete/<str:locate_id>/', Locate_Delete, name='Locate_Delete'),
]
