from django.urls import path
from Common.views import (HomeView, LoginView, LogoutView, UserListView)
from django.conf.urls.static import static
from django.conf import settings

app_name = 'Common'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserListView.as_view(), name='User_List'),
]
