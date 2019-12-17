"""sitetests URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from myaccount.views import Registration, UpdateAccount, logout_view, Login, activate
from mytest.views import index
from sitetests import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('tests/', include('mytest.urls'), name='tests'),
    path('registration/', Registration.as_view(), name='registration'),
    path('login/', Login.as_view(), name='login'),
    path('update/', UpdateAccount.as_view(), name='update'),
    path('logout/', logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('activate/<idb64>/<token>/', activate, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

