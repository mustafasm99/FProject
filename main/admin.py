from django.contrib         import admin , messages
from django.urls.resolvers  import URLPattern
from .models                import *
from django.urls            import reverse , path
from django.shortcuts       import render  , redirect
from django.http            import JsonResponse , HttpResponse
import pandas as pd 

# Register your models here.
class worksD(admin.ModelAdmin):
    list_display            = [ 'id' , 'teacher','emploeey' , 'studio_manger' , 'studio' , 'is_prove' ,'start_time' , 'end_time' , 'date' , 'cause' , 'type' , 'work_total_time' , 'get_teamleader' , 'ERORR']
    search_fields           = ['teacher__name' , 'emploeey__user__username' , 'studio_manger__user__username' , 'studio__name']
    list_filter             = ['studio' , 'cause' , 'type']
    change_list_template    = "admin/work.html"
    
    def get_urls(self) :
        urls =  super().get_urls()
        my_urls = [
            path('Get_excel/' , self.get_excels),
        ]
        return my_urls + urls
    
    def get_excels(self , request):
        try:
            Type = request.POST.get('Type')
            xslx = []
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
                    data_return     = []
                    all_users       = [i.username for i in User.objects.all()]
                    data_work_range = [i.get_user() if i.get_user() else None  for i in works.objects.filter(
                        date__range = [request.POST['from'] , request.POST['to']]
                    )
                                    ]
                    
                    for user in all_users:
                        if user not in data_work_range:
                            data_return.append(
                                {"User" : user}
                            )
                    excel = pd.DataFrame(data_return)
                    res = HttpResponse(content_type = 'application/ms-excel')
                    res['Content-Disposition'] = 'attachment; filename="No-work-users.xlsx"'
                    excel.to_excel(res , index=False , engine='openpyxl')
                    return res
                else:
                    data = works.objects.filter(
                        date__range = [request.POST['from'] , request.POST['to']],
                    )  
            
            
            for i in data:
                xslx.append(
                    {
                        "Id"            : i.id,
                        "Teacher"       : i.teacher,
                        "Emploeey"      : i.emploeey,
                        "Team Leader"   : i.get_teamleader(),
                        "Studio"        : i.studio ,
                        "Status"        : i.is_prove,
                        "Cause"         : i.cause ,
                        "Studio Manger" : i.studio_manger,
                        "Start Time"    : i.start_time,
                        "End Time"      : i.end_time,
                        "Total Time"    : i.work_total_time(),
                        "Date"          : i.date,
                        "Update"        : i.update,
                        "ERROR"         : i.ERORR,
                        
                    }
                )
            
            
            excel           = pd.DataFrame(xslx)
            
            res = HttpResponse(content_type = 'application/ms-excel')
            res['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            excel.to_excel(res , index=False , engine='openpyxl')
            return res
        except:
            messages.error(request , "يجب اختيار فلتر صالح ")
            return redirect("/admin/main/works")
    

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