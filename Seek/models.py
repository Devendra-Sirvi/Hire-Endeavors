from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class org(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile',
        null=True, blank=True, unique=True
    )
    orgname = models.CharField(
        max_length=50, blank=False, null=False, default="hello-org")
    managed_by = models.CharField(max_length=50, null=True)
    Description = models.TextField(null=True)
    Contact_Number = models.CharField(max_length=12, default="111111111111")
    Address = models.CharField(max_length=100,default="India")
    def __str__(self):
        return self.orgname if self.orgname else ''


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )
    Description = models.TextField(null=True)
    Residence = models.CharField(max_length=60, default="India")
    Contact = models.CharField(max_length=12, default="111111111111")


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        org.objects.create(user=instance)
        instance.profile.save()
        UserProfile.objects.create(user=instance)