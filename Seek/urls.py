from django.contrib import admin
from django.urls import path
from .views import index, Userregister, Orgregister
urlpatterns = [
    path('',index, name='index' ),
    path('user-reg/',Userregister),
    path('org-reg/',Orgregister)
]
