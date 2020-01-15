from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Activity.api.views import ActivitytList, ActivityDetail, StatusList, StatusDetail

urlpatterns = [
    path('activity/', ActivitytList.as_view(), name='activity_list'),
    path('activity/<str:pk>/', ActivityDetail.as_view(), name='activity_detail'),
    path('status/', StatusList.as_view(), name='status_list'),
    path('status/<str:pk>/', StatusDetail.as_view(), name='status_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
