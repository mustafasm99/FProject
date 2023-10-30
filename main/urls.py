from django.urls import path,include
from .views import *
urlpatterns = [
    path('home_teamleader',home_teamleader , name='teamleader'),
    path('New_emp',Create_employee,name='newemp'),
    path('check_username/<str:text>' , check_usernames , name='check_username'),
    path('home_emp' , home_emplooy , name='home_emp'),
    path('LOGOUT' , log_out , name='LOGOUT'),
    path('Nework' , New_work , name="nework"),
    path('get_teacher/<int:id>' , get_teacher , name='teachers'),
    path('requred' , Requred , name='requred'),
    path('home_studio' , home_studio , name="home_studio"),
    path('nework_studio' , nowork_studio , name='nework_studio'),
    path('tools' , tools , name='tools'),
    # path('excel' , from_excel , name="excel")
]
   