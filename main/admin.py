from django.contrib import admin
from django.urls.resolvers import URLPattern
from .models import *
from django.urls import reverse , path
from django.shortcuts import render
import pandas as pd 
from django.http import JsonResponse , HttpResponse

# Register your models here.
class worksD(admin.ModelAdmin):
    list_display = [ 'teacher','emploeey' , 'studio_manger' , 'studio' , 'is_prove' ,'start_time' , 'end_time' , 'date' , 'cause' , 'type' , 'work_total_time' , 'get_teamleader']
    search_fields = ['teacher' , 'emploeey' , 'studio_manger' , 'studio']
    list_filter = ['studio' , 'cause' , 'type']
    change_list_template = "admin/work.html"
    
    def get_urls(self) :
        urls =  super().get_urls()
        my_urls = [
            path('Get_excel/' , self.get_excels),
        ]
        return my_urls + urls
    
    def get_excels(self , request):
        Type = request.POST.get('Type')
        if request.POST.get('from') and request.POST.get("to"):
            if Type == "reject": 
                data = works.objects.filter(
                    date__range = [request.POST['from'] , request.POST['to']],
                    is_prove = False,
                )
            elif Type == "approve":
                data = works.objects.filter(
                    date__range = [request.POST['from'] , request.POST['to']],
                    is_prove = True,
                )
            elif Type == "Nowork":
                users = []
                data = data = works.objects.filter(
                    date__range = [request.POST['from'] , request.POST['to']]
                ).values("emploeey__user")
                for i in Emploeey.objects.all().values("user__id"):
                    if i not in data:
                        users.append(i)
                excel = pd.DataFrame(data)
                excel['emploeey__user'] = [
                    User.objects.filter(id = i['emploeey__user']).first() if not pd.isna(i) else " " for i in data
                ]
                res = HttpResponse(content_type = 'application/ms-excel')
                res['Content-Disposition'] = 'attachment; filename="No-work-users.xlsx"'
                excel.to_excel(res , index=False , engine='openpyxl')
                return res
            else:
                data = works.objects.filter(
                    date__range = [request.POST['from'] , request.POST['to']],
                )  
        
        excel = pd.DataFrame(data.values())
        teachers = []
        emploeeys = []
        studios = []
        types = []
        causes_names = []
        studio_mangers = []
        
        for index,i in enumerate(excel.iterrows()):
            teachers.append(teacher.objects.get(id = int(i[1]['teacher_id'])) if teacher.objects.filter(id = int(i[1]['teacher_id'])).first() else "No Teacher")
            emploeeys.append(
                Emploeey.objects.get(id = int(i[1]['emploeey_id']))
                if not pd.isna(i[1]['emploeey_id'])
                else "not Emploeey "
                )
            studios.append(
                studio.objects.get(id = int(i[1]['studio_id']))
                if not pd.isna(i[1]['studio_id']) 
                else "Not studio"
                )
            types.append(works_type.objects.filter(id = int(i[1]['type_id'])).first() if not pd.isna(i[1]['type_id']) else " ")
            causes_names.append(
              causes.objects.filter(
              id = int(i[1]['cause_id'])).first()
              if not pd.isna(i[1]['cause_id'])
              else " "
            )
            studio_mangers.append(
                studio_manger.objects.filter(id = int(i[1]['studio_manger_id'])).first()
                if not pd.isna(i[1]['studio_manger_id'])
                else " "
            )
        excel['teacher_id'] = teachers
        excel['emploeey_id'] = emploeeys
        excel['type_id'] = types
        excel['cause_id'] = causes_names
        excel['studio_manger_id'] = studio_mangers
        
        res = HttpResponse(content_type = 'application/ms-excel')
        res['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
        excel.to_excel(res , index=False , engine='openpyxl')
        return res
        print(excel)
        return JsonResponse(list(data.values()) , safe=False)
    

class studioD(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    change_list_template = "admin/studio.html"
    

    def get_urls(self):
        urls = super(studioD , self).get_urls()
        custom_urls = [
            path('tools/', self.tools, name='admin-tools'),
        ]
        return custom_urls + urls

    def tools(self, request):
        if request.method == "POST":
            print(request.POST, "POSTING")
        print("GET")
        return render(request, "Tools/studio.html")


class EmploeeyD(admin.ModelAdmin):
    list_display = ['user' , 'display' , 'teamleader' , 'all_works']
    search_fields = ['user_username' , 'teamleader']
    list_filter = ['teamleader']
    change_list_template = "admin/emp.html"

admin.site.register(Emploeey , EmploeeyD)
admin.site.register(teamleader)
admin.site.register(teacher)
admin.site.register(stages)
admin.site.register(materials)
admin.site.register(works , worksD)
admin.site.register(works_type)
admin.site.register(studio , studioD )
admin.site.register(studio_manger)
admin.site.register(causes)