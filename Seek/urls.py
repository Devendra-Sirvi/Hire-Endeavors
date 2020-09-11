from django.contrib import admin
from django.urls import path
from .views import (index, Userregister, Orgregister,
                    confirmation, createorgpost, createuserpost)


urlpatterns = [
    path('', index, name='index'),
    path('user-reg/', Userregister),
    path('org-reg/', Orgregister),
    path('create-user-post/', createuserpost, name='user-post'),
    path('create-org-post/', createorgpost, name='org-post'),
    path('confirmation/', confirmation, name='confirm')
]