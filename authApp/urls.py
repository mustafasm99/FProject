from django.urls import path,include
from .views import *


urlpatterns = [
    path('',login_page,name="home"),
]