from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import loginuser, register, logout_view, search_results

urlpatterns = [
    path('', loginuser, name = 'login' ),
    path('register/', register, name = 'register'),  
    url(r'^search/', search_results, name = 'search_users'),
    path('logout', logout_view, name='logout'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
