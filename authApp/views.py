from django.shortcuts import render , redirect
from django.contrib.auth import login,logout, authenticate
from main.models import *
# Create your views here.


def login_page(e):
    if e.method == 'POST':
        print(e.POST)
        username = e.POST.get('username')
        password = e.POST.get('password')

        user = authenticate(e , username=username , password = password)
        if user:
            login(e , user)
            if Emploeey.objects.filter(user = user).first():
                return redirect("/home_emp")
            return redirect("/home_teamleader")
    return render(e , 'authApp/home.html')
    
