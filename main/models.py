from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Emploeey(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='eimages/')
    teamleader = models.ForeignKey("teamleader" , on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    #   function for get all self works 
    def get_all_works(self):
        return works.objects.filter(emploeey = self).all()
    
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
        ).all()

class teacher(models.Model):
    name = models.CharField(max_length=120 )
    image = models.ImageField(upload_to="timage/")
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
    emploeey = models.ForeignKey('emploeey' , on_delete=models.CASCADE)
    is_prove = models.BooleanField()
    date = models.DateField(auto_now=True)
    type = models.ForeignKey(works_type, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.emploeey.user.username} -> {self.teacher.name} | AT : {self.date} \n start time : {self.start_time} \n end time : {self.end_time}"
    
    def work_total_time(self):
        return self.start_time - self.end_time

    def __add__(self , obj):
        return self.work_total_time + obj.work_total_time
    
    def get_teamleader(self):
        return  teamleader.objects.filter(
            id = self.emploeey.teamleader,
        ).first()