from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class userjobpost(models.Model):
    Position_Name = models.CharField(max_length=50, default="Job_Name")
    Description = models.TextField(max_length=200, default="Job_Desc")
    Expected_Salary = models.IntegerField(default=0)
    age = models.IntegerField(default=18)
    Exp = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userpost',
        null=True, blank=True, unique=False
    )

    def __str__(self):
        return self.Position_Name


class orgjobpost(models.Model):
    Position_Name = models.CharField(max_length=50, default="Job_Name")
    Description = models.TextField(max_length=200, default="Job_Desc")
    Salary = models.IntegerField(default=0)
    age = models.IntegerField(default=18)
    Exp = models.IntegerField(default=0)
    No_of_openings = models.IntegerField(default=0)
    Job_Site_Address = models.CharField(max_length=60, default="India")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orgpost',
        null=True, blank=True, unique=False
    )

    def __str__(self):
        return self.Position_Name
