from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import login , logout , authenticate
from .models import*
from django.contrib.auth.models import User
from django.http import JsonResponse , HttpResponse
import datetime
import pandas as pd
# Create your views here.


def home_teamleader(e):
    # the post Request  <------------->
    if e.method == "POST":
        print(e.POST)
        if teamleader.objects.filter(user = e.user):
            # the action to delete the user 
            if e.POST.get('delete'):
                Emploeey.objects.get(id =e.POST['id']).user.delete()
                return redirect('/home_teamleader')
            # the action to make the request aprove 
            if e.POST.get('toaprove'):
                print('hi')
                prove = works.objects.get(id = e.POST['toaprove'])
                prove.is_prove = True 
                prove.save()
            # the action to make the request rejected 
            if e.POST.get('toareject'):
                reject = works.objects.get(id = e.POST['toareject'])
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
            'emp':emp,
            'teachers':teacher.objects.all(),
            'sub':materials.objects.all()
        })
    else:
        return redirect('/')

# these function for get the teacher info API 
def get_teacher(e,id):
    if teacher.objects.filter(id = id).first().image:
        data = teacher.objects.filter(id = id ).values("name" , "image" ,"id").first()
    else:
        data = teacher.objects.filter( id = id ).values("name" , "id").first()
        data['image'] = "acc.jpg"
    return JsonResponse({
        "teacher":data
    })


# Requred API for start end and creates the works 
def Requred(e):
    if e.GET.get('state'):
        if e.GET.get('state') == 'running':
            if 'start_time' in e.session:
                e.session['start_time'] = ''
                e.session.modified = True
            e.session['start_time'] = datetime.datetime.now().time().strftime("%H:%M:%S")
            return JsonResponse({
                'state':'start record',
                'start_at':e.session['start_time']
            })
        elif e.GET.get('state') == "stop":
            print(e.GET)
            if 'start_time' in e.session:
                end_time = datetime.datetime.now().time().strftime("%H:%M:%S")
                # print(end_time , e.session['start_time'])
                try:
                    works.objects.create(
                        start_time = e.session['start_time'],
                        end_time = end_time,
                        emploeey = Emploeey.objects.get(user = e.user) if Emploeey.objects.filter(user = e.user).first() else None,
                        type = works_type.objects.filter(id = 1).first(),
                        teacher = teacher.objects.filter(id = e.GET.get('teacher')).first(),
                        is_prove = None,
                        studio = studio.objects.get(id = int(e.GET.get('studio'))) if e.GET.get('studio') and e.GET.get('studio') is not None  else None ,
                        cause = causes.objects.get(id = int(e.GET.get('case'))) if e.GET.get('case') and e.GET.get('case') is not None  else None ,
                        studio_manger = studio_manger.objects.get(user = e.user) if studio_manger.objects.filter(user = e.user).first() else None
                    )
                    totalTime = datetime.datetime.strptime(end_time ,"%H:%M:%S")- datetime.datetime.strptime(e.session['start_time'] , "%H:%M:%S")
                    hours,teminder = divmod(totalTime.seconds , 3600)
                    minutes , secondes = divmod(teminder , 60)
                    if Emploeey.objects.filter(user = e.user):
                        return JsonResponse({
                            'state':'done',
                            'end_time':end_time,
                            'start_time':e.session['start_time'],
                            'Total_requred': f"{hours}:{minutes}:{secondes}"
                        })
                    else:
                        return JsonResponse({
                            'state':'done',
                            'end_time':end_time,
                            'start_time':e.session['start_time'],
                            'Total_requred': f"{hours}:{minutes}:{secondes}",
                            'studio': studio.objects.get(id = int(e.GET.get('studio'))).name if e.GET.get('studio') and e.GET.get('studio') is not None  else None ,
                            'cause': causes.objects.get(id = int(e.GET.get('case'))).name if e.GET.get('case') and e.GET.get('case') is not None  else None ,
                        })
                except:
                    print(e.GET)
                    return JsonResponse({
                        'state':'you didnt select any teacher'
                    })
    return JsonResponse({
        "state":"no state sended"
    })


def home_studio(e):
    stu_mang = studio_manger.objects.filter(user = e.user).first()
    if stu_mang:
        return render(e , "main/home_studio.html" ,{'data':stu_mang})
    else:
        return redirect('/')
def nowork_studio(e):
    return render(e , 'main/nework_studio.html' , {
        'data':studio_manger.objects.filter(user = e.user).first(),
        'studios':studio.objects.all(),
        'causes':causes.objects.all(),
        'teachers':teacher.objects.all(),
        'sub':materials.objects.all()
    })


#//////////////////////////////////////////////////////
#///////////// admin page veiws ///////////////////////
#/////////////////////////////////////////////////////
def tools(e):
    if e.method == "POST":
        if e.POST.get('studio'):
            st = studio.objects.all()
            data_set = []
            for studio_instance in st:
                for work_instance in studio_instance.get_all_works():
                    data_set.append({
                        'id': work_instance.id,
                        'start_time': work_instance.start_time,
                        'end_time': work_instance.end_time,
                        'total_time': work_instance.work_total_time(),
                        'teacher': work_instance.get_teacher(),
                        'is_prove': work_instance.is_prove,
                        'studio': work_instance.get_studio(),
                        'type': work_instance.get_type(),
                        'cause': work_instance.get_cause(),
                        'manager': work_instance.get_manager(),
                    })
                data_set.append({'End section for ' : studio_instance.name})
            data = pd.DataFrame(data_set)
            res = HttpResponse(content_type = "application/ms-excel")
            res['Content-Disposition'] = f'attachemnt; filename = {datetime.datetime.now().strftime("%Y_%M_%D|%H_%M_%S")}.xlsx'
            data.to_excel(res, index=False)
            return res
        
        
        elif e.POST.get('emp'):
            emps = Emploeey.objects.all()
            data = []
            for i in emps:
                for j in i.get_all_works():
                    data.append({
                        'work_id': j.id,
                        'Emploeey': j.emploeey.user.username,
                        'start_time': j.start_time,
                        'end_time': j.end_time,
                        # 'total_time': j.work_total_time(),
                        'teacher': j.get_teacher(),
                        'is_prove': j.is_prove,
                        'date': j.date
                    })
                data.append({"End section for" : f"{i.user.username}"})
                
            data_frame = pd.DataFrame(data)
            res = HttpResponse(content_type = "application/ms-excel")
            res['Content-Disposition'] = f'attachemnt; filename = {datetime.datetime.now().strftime("%Y_%M_%D|%H_%M_%S")}.xlsx'
            data_frame.to_excel(res, index=False)
            return res
            # return JsonResponse(data , safe=False)

        elif e.POST['work']:
            Type = e.POST.get("Type")
            if  Type == "reject":
                data = works.objects.filter(is_prove = False).all() 
            elif Type == "approv":
                data = works.objects.filter(is_prove = True).all()
            elif Type == "Nowork":
                data = []
                for i in Emploeey.objects.all():
                    if len(i.get_all_works()) == 0:
                        data.append({"user":i.user.username})
                frame = pd.DataFrame(data)
                res = HttpResponse(content_type = "application/ms-excel")
                res['Content-Disposition'] = f'attachemnt; filename = Work_{datetime.datetime.now().strftime("%Y_%M_%D|%H_%M_%S")}.xlsx'
                frame.to_excel(res, index=False)
                return res
            else :
                data = works.objects.all()
            temp = []
            for i in data:
                toFrame = {
                    'id':i.id,
                    'Teacher':i.teacher,
                    'Emploeey':i.emploeey,
                    'Studio manger': i.studio_manger,
                    'studio':i.studio,
                    'start_time':i.start_time,
                    'end_time':i.end_time,
                    'total time':i.work_total_time(),
                    'date':i.date,
                    'cause':i.cause,
                    'type':i.type,
                    'Team leader':i.get_teamleader(),
                    "State":i.is_prove
                }
                temp.append(toFrame)
            frame = pd.DataFrame(temp)
            res = HttpResponse(content_type = "application/ms-excel")
            res['Content-Disposition'] = f'attachemnt; filename = Work_{datetime.datetime.now().strftime("%Y_%M_%D|%H_%M_%S")}.xlsx'
            frame.to_excel(res, index=False)
            return res
        else:
            HttpResponse("BAND REQUEST")
    else:
        return HttpResponse("ERORR")
   
   
# code for uploads users with excel 
   
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path 
    
def from_excel(e):
    from FProject.settings import BASE_DIR
    file = BASE_DIR/'static/Users.xlsx'
    p = pd.read_excel(file , sheet_name='Sheet2')
    passwords = []
    img = BASE_DIR/'static/img/acc.jpg'
    image_file = SimpleUploadedFile(name=img.name, content=open(str(img), 'rb').read())
    for index , i in enumerate(p['Production']):
        try:
            full_name = i.strip().split(" ")
            # print(full_name)
            passwords.append({
                "user name": full_name[0]+"_"+full_name[1],
                "password" : full_name[0]+full_name[1]+str(index+1)
                
                })  
        
            user = User.objects.create_user(
                username=full_name[0]+"_"+full_name[1],
                first_name = full_name[0],
                last_name = full_name[1],
                password=full_name[0]+full_name[1]+str(index+1)
            )
        
            Emploeey.objects.create(
                user = user,
                image = image_file,
                teamleader = teamleader.objects.filter(user = User.objects.filter(username = "Production").first()).first()
            )
        except:
            pass
        
    newExcel = pd.DataFrame(passwords)
    
    res = HttpResponse(content_type = "application/ms-excel")
    res['Content-Disposition'] = f'attachemnt; filename = Production.xlsx'
    newExcel.to_excel(res, index=False)
    return res
    
    return HttpResponse("done")


def filter_works(e):
    if e.method == "GET":
        print(e.GET)
        
        if "approve" in e.GET:
            data = teamleader.objects.filter(user = e.user).first()
            return render(e , "main/filter.html" , {"teamleader":data.get_all_Aprove() , "teamleaderUser":data})
        elif "reject" in e.GET:
            data = teamleader.objects.filter(user = e.user).first()
            return render(e , "main/filter.html" , {"teamleader":data.get_all_Reject() , "teamleaderUser":data})
        elif "Employes" in e.GET:
            data = teamleader.objects.filter(user =e.user).first()
            return render(e,"main/employes.html",{"data":data.get_all_emploey()})
    else:
        return JsonResponse({"stats":"no POST Request"})