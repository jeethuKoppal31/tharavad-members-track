from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager



# Create your models here.
class Groups(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null= True)
    pin = models.CharField(max_length=20, blank=True, null=True)
    
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Groups"

    def __str__(self):
        return str(f"{self.name}")

class Members(models.Model):
    code = models.CharField(max_length=250)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    middle_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250)
    mother = models.CharField(max_length=250)
    father = models.CharField(max_length=250)
    grandma = models.CharField(max_length=250)
    thaivazhi = models.CharField(max_length=250) 
    gender = models.CharField(max_length=20, choices=(('Male','Male'), ('Female','Female')), default = "Male")
    marital_status = models.CharField(max_length=20, choices=(('Single','Single'), ('Married','Married'), ('Divorced','Divorced'), ('Widowed','Widowed')), default = "Single")
    education = models.CharField(max_length=250)
    contact = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    address = models.TextField(blank=True, null= True)
    image_path = models.ImageField(upload_to="members/",blank=True, null=True)
    status = models.CharField(max_length=2, choices=(('1','Active'), ('2','Inactive')), default = 1)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Members"

    def __str__(self):
        return str(f"{self.code} - {self.first_name}{' '+self.middle_name if not self.middle_name == None else ''} {self.last_name}")

    def name(self):
        return str(f"{self.first_name}{' '+self.middle_name if not self.middle_name == None else ''} {self.last_name}")

    def save(self):
        super().save()
        img = Image.open(self.image_path.path) 
        if img.height > 300 or img.width > 300:
            new_img = (300, 300)
            img.thumbnail(new_img)
            img.save(self.image_path.path)  
