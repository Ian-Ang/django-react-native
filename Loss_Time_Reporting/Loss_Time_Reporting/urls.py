"""Loss_Time_Reporting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Common.views import handler404, handler500

app_name = 'Loss_Time_Reporting'

urlpatterns = [
    #api authenticate
    path('api-auth/', include('rest_framework.urls')),

    #Path for Web Admin
    path('admin/', admin.site.urls),
    path('', include('Common.urls', namespace="Common")),
    path('', include('django.contrib.auth.urls')),
    path('supervisor/', include('Supervisor.urls', namespace="Supervisor")),
    path('staff/', include('Staff.urls', namespace='Staff')),
    path('activity/', include('Activity.urls', namespace="Activity")),
    path('equipment/', include('Equipment.urls', namespace="Equipment")),
    path('teams/', include('Teams.urls', namespace="Teams")),

    # Path REST API for Mobile React Native
    path('api_user/', include('Common.api.urls')),
    path('api_equipment/', include('Equipment.api.urls')),
    path('api_activity/', include('Activity.api.urls')),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404
handler500 = handler500
