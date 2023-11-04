from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.safestring import mark_safe
# Create your models here.

class Emploeey(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='eimages/')
    teamleader = models.ForeignKey("teamleader" , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    #   function for get all self works 
    def get_all_works(self):
        return works.objects.filter(emploeey = self).all().order_by('-id') if works.objects.filter(emploeey = self).first() else []
    
    #   function for get all self rejected works 
    def get_rejected_works(self):
        return works.objects.filter(
            is_prove = False,
            emploeey = self,
        ).all()
    
    #   function for geting self data for aproved works 
    def get_all_aprove_work(self):
        return works.objects.filter(
            is_prove = True ,
            emploeey = self
        ).all()
    
    def all_works(self):
        html = "<ul>"
        for i in self.get_all_works():
            html += f"<li>{i}</li>"
        html += "<ul>"
        return mark_safe(html)

    def display(self):
        html = f"<img src='{self.image.url if self.image else None}' width='100' height='100' style='object-fit:cover;'>"
        return mark_safe(html)

    
class teamleader(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='timages/')

    def __str__(self):
        return self.user.username
    
    def get_all_emploey(self):
        return Emploeey.objects.filter(teamleader = self).all()
    
    def get_all_Requests(self):
        return works.objects.filter(
            emploeey__in = self.get_all_emploey()
        ).all().order_by('-id')
    def get_all_Aprove(self):
        return works.objects.filter(
            emploeey__in = self.get_all_emploey(),
            is_prove = True
        )
    def get_all_Reject(self):
        return works.objects.filter(
            emploeey__in = self.get_all_emploey(),
            is_prove = False
        )
class teacher(models.Model):
    name = models.CharField(max_length=120 )
    image = models.ImageField(upload_to="timage/" , null=True , blank=True)
    stage = models.ForeignKey('stages' , on_delete=models.CASCADE)
    materials = models.ForeignKey('materials' , on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_totals_works_time(self):
        import time
        total = time()
        for work in works.objects.filter(teacher = self).all():
            total += work.work_total_time()
        return total
    
    def get_last_work_info(self):
        return works.objects.filter(teacher = self).first()


class stages(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class materials(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class works_type(models.Model):
    title = models.CharField(max_length=120 , help_text="Note if u delete this all works that done with it will be deleted `(*>﹏<*)′")

    def __str__(self):
        return self.title

class works(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey('teacher' , on_delete=models.CASCADE)
    emploeey = models.ForeignKey('emploeey' , on_delete=models.CASCADE , null=True , blank=True)
    is_prove = models.BooleanField(blank=True , null=True , default=None)
    date = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)
    studio = models.ForeignKey('studio' , on_delete=models.CASCADE , null=True , blank=True)
    type = models.ForeignKey(works_type, on_delete=models.CASCADE)
    cause = models.ForeignKey('causes' , on_delete=models.CASCADE , null=True , blank=True)
    studio_manger = models.ForeignKey("studio_manger", null=True , blank=True , on_delete=models.CASCADE)

    def __str__(self):
        user = None 
        if self.emploeey:
            user = self.emploeey.user.username
        elif self.studio_manger:
            user = self.studio_manger.user.username
        else:
            user = "NO USER"
        return f"{user} -> {self.teacher.name} | AT : {self.date} \n start time : {self.start_time} \n end time : {self.end_time}"
    
    def work_total_time(self):
        # start_time = datetime.strptime(str(self.start_time), "%H:%M:%S").time()
        # end_time = datetime.strptime(str(self.end_time), "%H:%M:%S").time()
        start_time = self.start_time
        end_time = self.end_time
        total_seconds = (datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).seconds

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours}:{minutes}:{seconds}"

    def __add__(self , obj):
        return datetime.strptime(self.work_total_time , "%H:%M:%S") + datetime.strptime(obj.work_total_time , "%H:%M:%S")
    
    def get_teamleader(self):
        x = teamleader.objects.filter(
            id = self.emploeey.teamleader.id,
        ).first() if self.emploeey else 'no teamleader'
        return x
    
    def get_manager(self):
        return self.studio_manger.user.username if self.studio_manger else "no manger work not studio"
    
    def get_cause(self):
        return self.cause.name if self.cause else None
    
    def get_type(self):
        return self.type.title if self.type else None
    
    def get_studio(self):
        return self.studio.name if self.studio else None 
    
    def get_teacher(self):
        return self.teacher.name

class studio(models.Model):
    name = models.CharField(max_length=50)

    def get_total_work_time(self):
        total_time = ''
        work = works.objects.filter(studio = self).all()
        for i in work:
            total_time += i.work_total_time()
        return total_time
    
    def get_all_works(self):
        return works.objects.filter(studio = self).all()

    def __str__(self):
        return self.name
    


    
class causes(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class studio_manger(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to="studio_manger/")
    # studio = models.OneToOneField('studio' , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def get_all_works(self):
        return works.objects.filter(studio_manger = self).all().order_by('-id')
    


