from django.urls import path
from Common.views import (HomeView, LoginView, LogoutView, UserListView, CreateUserView, ProfileView)
from django.conf.urls.static import static
from django.conf import settings

app_name = 'Common'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserListView.as_view(), name='user_list'),
    path('create/', CreateUserView.as_view(), name='created_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
