from django.shortcuts import render
from .forms import (RegistrationForm, OrgRegistrationForm, OrgProfileform)
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .models import org

# Create your views here.
def index(request):
    return render(request, "Seek/index.html")

def Userregister(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()

    context = {'form': form, 'titl':"User Sign-up"}
    return render(request, 'registration/user-registration.html', context)

def Orgregister(request):
    if request.method == 'POST':
        form = OrgRegistrationForm(request.POST)
        profile_form = OrgProfileform(request.POST)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            name = profile_form.cleaned_data['Organisation']
            mng = profile_form.cleaned_data['Manager']
            desc = profile_form.cleaned_data['Description']
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = org.objects.get(user=user)
            profile.orgname = name
            profile.managed_by = mng
            profile.Description = desc
            profile.save()
            return redirect('index')
    else:
        form = OrgRegistrationForm()
        profile_form = OrgProfileform()

    context = {'form': form,'profile_form': profile_form, 'titl': "Organisation Sign-Up"}
    return render(request, 'registration/org-registration.html', context)