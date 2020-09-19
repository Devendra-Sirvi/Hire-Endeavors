from django.contrib import admin
from django.urls import path
from django.conf.urls import handler400
from Seek import views as myapp_views
from .views import (getstart, index, Userregister, Orgregister, UserProfileDetailView, OrgProfileDetailView,
                    confirmation, createorgpost, createuserpost, card, clientconsent, profile_org, profile_user, UserUpdatation, OrgUpdatation, post_by_users, post_by_orgs)


urlpatterns = [
    path('', index, name='index'),
    path('Get-Started/', getstart),
    path('user-reg/', Userregister),
    path('org-reg/', Orgregister),
    path('create-user-post/', createuserpost, name='user-post'),
    path('create-org-post/', createorgpost, name='org-post'),
    path('confirmation/', confirmation, name='confirm'),
    path('card/', card),
    path('consent/', clientconsent),
    path('user-profile/', profile_user, name="user-profile"),
    path('org-profile/<int:pk>/', OrgProfileDetailView.as_view(), name="oprofile"),
    path('user-profile/<int:pk>/', UserProfileDetailView.as_view(), name="uprofile"),
    path('org-profile/', profile_org, name="org-profile"),
    path('user-update/', UserUpdatation),
    path('org-update/', OrgUpdatation),
    path('byusers/', post_by_users),
    path('byorgs/', post_by_orgs),
    
]


