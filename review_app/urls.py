from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import OneProfile, OneProject, loginuser, my_profile, project, rate, register, logout_view, search_results, HomeView, HomeView2, UpdateProjectView, UpdateProfileView, ProjectList, ProfileList
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', loginuser, name = 'login' ),
    path('register/', register, name = 'register'), 
    path('home/', HomeView, name = 'home'), 
    path('project/<int:pk>', project, name = 'project'), 
    path('project/review/<int:pk>', rate, name = 'rate'), 
    path('profile', my_profile, name = 'profile'),
    path('update/project/<int:pk>', UpdateProjectView.as_view(), name = 'update_project'),
    path('update/profile/<int:pk>', UpdateProfileView.as_view(), name = 'update_profile'),
    path('search/', search_results, name = 'search_users'),
    path('reviews/api/projects/', ProjectList.as_view()),
    path('reviews/api/profiles/', ProfileList.as_view()),
    path('api-token-auth/', obtain_auth_token),
    path('api/project/<int:pk>/',OneProject.as_view()),
    path('api/profile/<int:pk>/',OneProfile.as_view()),
    path('logout', logout_view, name='logout'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
