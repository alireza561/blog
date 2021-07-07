"""config2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from account.views import Login, PasswordChange, PasswordChangeDone, Register, activate
from config2.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comment/', include('comment.urls')),
    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    path('', home, name='home'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDone.as_view(), name='password_change_done'),
    path('', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
    path('', include('category.urls')),
    path('account/', include('account.urls')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
