from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from .models import*
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.


def home_teamleader(e):
    # the post Request  <------------->
    if e.method == "POST":
        if teamleader.objects.filter(user = e.user):
            # the action to delete the user 
            if e.POST.get('delete'):
                Emploeey.objects.get(id =e.POST['id']).user.delete()
                return redirect('/home_teamleader')
            # the action to make the request aprove 
            if e.POST.get('toaprove'):
                prove = works.objects.get(id = e.POST['toaprove'])
                prove.is_prove = True 
                prove.save()
            # the action to make the request rejected 
            if e.POST.get('toreject'):
                reject = works.objects.get(id = e.POST['toreject'])
                reject.is_prove = False
                reject.save()
        else:
            messages.add_message(e , messages.ERROR , "the user is not the teamleader (❁´◡`❁)")
    # the get Request <----------------->
    # if e.user.is_authenticated:
    teamleaderx = teamleader.objects.filter(user = e.user).first()
    data = {
        'teamleader':teamleaderx,
    }
    return render(e , 'main/home.html' , data)

def Create_employee(e):
    if e.method == "POST":
        # crate the data frame 
        user_name = e.POST.get('username')
        first_name = e.POST.get('firstname')
        last_name = e.POST.get('lastname')
        email = e.POST.get('email')
        password = e.POST.get('password')
        # create the USER 
        new =  User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username=user_name,
            password=password,
            email=email
        )
        new.save()
        # create the EMPLOEY
        Emploeey.objects.create(
            user = new,
            image = e.FILES.get('image'),
            teamleader = teamleader.objects.filter(user = e.user).first(),
        ).save()
        #done Create the Emploeey 
        return redirect('/home_teamleader')
    return render(e ,'main/create_user.html' , {'teamleader':teamleader.objects.filter(user = e.user).first()})

# the API to check if the user name been used or not 

def check_usernames(e , text):
    exc = User.objects.filter(username__exact = text)
    return JsonResponse({
        'user':exc.values('date_joined' , 'email' , 'first_name' , 'last_name' , 'username' , 'last_login').first() if exc else False,
    })

def log_out(e):
    logout(e)
    return redirect('/')

def home_emplooy(e):
    emp = Emploeey.objects.filter(user = e.user).first()
    if emp:
        return render(e , 'main/home_emp.html' , {
            'emp':emp
        })
    else:
        return redirect('/')

def New_work(e):
    emp = Emploeey.objects.filter(user = e.user).first()
    if emp:
        return render(e , "main/nework.html" , {
            'emp':emp
        })
    else:
        return redirect('/')