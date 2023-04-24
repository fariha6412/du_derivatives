from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from base.views import *

from base.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', loginUser, name='login'),
    path('logout', logoutUser, name='logout'),
    path('signup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('addProject', addProject, name='addProject'),
    path('projectPage-<str:pk>', projectPage, name='projectPage'),

    path('appDetails', appDetails, name='appDetails'),
]