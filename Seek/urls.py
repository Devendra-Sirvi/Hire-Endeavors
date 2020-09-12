from django.contrib import admin
from django.urls import path
from .views import (index, Userregister, Orgregister,
                    confirmation, createorgpost, createuserpost, card, clientconsent, profile_org, profile_user, UserUpdatation, OrgUpdatation, post_by_users)


urlpatterns = [
    path('', index, name='index'),
    path('user-reg/', Userregister),
    path('org-reg/', Orgregister),
    path('create-user-post/', createuserpost, name='user-post'),
    path('create-org-post/', createorgpost, name='org-post'),
    path('confirmation/', confirmation, name='confirm'),
    path('card/', card),
    path('consent/', clientconsent),
    path('user-profile/', profile_user, name="user-profile"),
    path('org-profile/', profile_org, name="org-profile"),
    path('user-update/', UserUpdatation),
    path('org-update/', OrgUpdatation),
    path('byusers/', post_by_users)
]

