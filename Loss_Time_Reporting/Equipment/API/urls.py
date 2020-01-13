from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Equipment.API.views import EquipmentList, EquipmentDetail, LocateList, LocateDetail

urlpatterns = [
    path('equipment/', EquipmentList.as_view(), name='equipment_list'),
    path('equipment/<str:pk>/', EquipmentDetail.as_view(), name='equipment_detail'),
    path('locate/', LocateList.as_view(), name='locate_list'),
    path('locate/<str:pk>/', LocateDetail.as_view(), name='locate_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
