from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Common.api.views import UsertList, UserDetail, AddressList, AddressDetail

urlpatterns = [
    path('user/', UsertList.as_view(), name='user_list'),
    path('user/<str:pk>/', UserDetail.as_view(), name='user_detail'),
    path('address/', AddressList.as_view(), name='address_list'),
    path('address/<int:pk>/', AddressDetail.as_view(), name='address_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
