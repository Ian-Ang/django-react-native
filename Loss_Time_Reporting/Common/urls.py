from django.urls import path
from Common.views import (HomeView, LoginView, LogoutView, UserListView, CreateUserView, ProfileView, UserDeleteView, UserDetailView, UpdateUserView)
from django.conf.urls.static import static
from django.conf import settings

app_name = 'Common'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/list/', UserListView.as_view(), name='user_list'),
    path('user/create/', CreateUserView.as_view(), name='created_user'),
    path('user/profile/', ProfileView.as_view(), name='profile'),
    path('user/<int:pk>/edit/', UpdateUserView.as_view(), name='update'),
    path('user/<int:pk>/view/', UserDetailView.as_view(), name='detail'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]
