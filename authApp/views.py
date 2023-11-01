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
            if Emploeey.objects.filter(user = e.user).first():
                return redirect("/home_emp")
            if studio_manger.objects.filter(user = e.user).first():
                return redirect("/home_studio")
            return redirect("/home_teamleader")
    if not e.user.is_authenticated:
        return render(e , 'authApp/home.html')
    else:
        if Emploeey.objects.filter(user = e.user).first():
            return redirect("/home_emp")
        elif studio_manger.objects.filter(user = e.user).first():
            return redirect("/home_studio")
        elif teamleader.objects.filter(user = e.user).first():
            return redirect('/home_teamleader')
        else:
            logout(e)
            return render(e , 'authApp/home.html')


    
