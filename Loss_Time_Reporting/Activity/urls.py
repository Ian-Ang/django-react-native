from django.urls import path
from Activity.views import *

app_name = 'Activity'

urlpatterns = [
    path('', Activity_List, name='Activity_List'),
    path('create/', Activity_Create, name='Activity_Create'),
    path('detail/<str:activity_id>/', Activity_Detail, name='Activity_Detail'),
    path('edit/<str:activity_id>/', Activity_Edit, name='Activity_Edit'),
    path('delete/<str:activity_id>/', Activity_Delete, name='Activity_Delete'),
    path('status/', Status_List, name='Status_List'),
    path('status_create/', Status_Create, name='Status_Create'),
    path('status_detail/<str:status_id>/', Status_Detail, name='Status_Detail'),
    path('status_edit/<str:status_id>/', Status_Edit, name='Status_Edit'),
    path('status_delete/<str:status_id>/', Status_Delete, name='Status_Delete'),
]
