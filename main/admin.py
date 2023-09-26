from django.contrib import admin
from .models import *
from django.urls import reverse , path
from django.shortcuts import render

# Register your models here.
class worksD(admin.ModelAdmin):
    list_display = [ 'teacher','emploeey' , 'studio_manger' , 'studio' ,'start_time' , 'end_time' , 'date' , 'cause' , 'type' , 'work_total_time' , 'get_teamleader']
    search_fields = ['teacher' , 'emploeey' , 'studio_manger' , 'studio']
    list_filter = ['studio' , 'cause' , 'type']
    change_list_template = "admin/work.html"

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
    search_fields = ['user','teamleader']
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