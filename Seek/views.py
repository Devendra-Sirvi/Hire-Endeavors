from django.shortcuts import render
from .forms import (RegistrationForm, OrgRegistrationForm,
                    OrgProfileform, UserJobPost, OrgJobPost, confirm)
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import org
from jobs.models import userjobpost, orgjobpost
# Create your views here.


def index(request):
    data = None
    if request.user.is_authenticated:
        me = request.user.username
        you = f"Welcome {me}, we hope that you find your best suited job! Best of Luck!"
        messages.info(request, you)
        u = userjobpost.objects.all()
        o = orgjobpost.objects.all()

        data = {'user_obj': u, 'org_obj': o}
    return render(request, "Seek/index.html", data if data else None)


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
        # form = RegistrationForm()
        form = UserJobPost()

    context = {'form': form, 'titl': "User Sign-up"}
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
            profile.We_Are = "org"
            profile.orgname = name
            profile.managed_by = mng
            profile.Description = desc
            profile.save()
            return redirect('index')
    else:
        form = OrgRegistrationForm()
        profile_form = OrgProfileform()

    context = {'form': form, 'profile_form': profile_form,
               'titl': "Organisation Sign-Up"}
    return render(request, 'registration/org-registration.html', context)


def createuserpost(request):
    if request.method == "POST":
        form = UserJobPost(request.POST)

        if form.is_valid():
            #form.save()
            p = userjobpost()
            p.Position_Name = form.cleaned_data['Position_Name']
            p.Description = form.cleaned_data['Description'] 
            p.Expected_Salary = form.cleaned_data['Expected_Salary'] 
            p.age = form.cleaned_data['Age']
            p.Exp = form.cleaned_data['Experience']
            p.created_by = request.user 
            p.save()
            return redirect('index')

    else:
        form = UserJobPost()
    
    context = {'form':form, 'titl': "Request Job Post", 'act':"/create-user-post/"}
    return render(request, "Seek/post.html", context)

def createorgpost(request):
    if request.method == "POST":
        form = OrgJobPost(request.POST)

        if form.is_valid():
            #form.save()
            p = orgjobpost()
            p.Position_Name = form.cleaned_data['Position_Name']
            p.Description = form.cleaned_data['Description'] 
            p.Salary = form.cleaned_data['Salary'] 
            p.age = form.cleaned_data['Age_Criteria']
            p.No_of_openings = form.cleaned_data['Number_Of_Openings']
            p.Exp = form.cleaned_data['Minimum_required_experience']
            p.created_by = request.user 
            p.save()
            return redirect('index')
    else:
        form = OrgJobPost()
    
    context = {'form':form, 'titl': "Publish Job Post", 'act':"/create-org-post/"}
    return render(request, "Seek/post.html", context)

def confirmation(request):
    if request.method == "POST":
        form = confirm(request.POST)

        if form.is_valid():
            op1 = form.cleaned_data['Want_to_hire']
            op2 = form.cleaned_data['Seeking_Jobs']
            if(op1 is True and op2 is False):
                return redirect('org-post')

            elif(op2 is True and op1 is False):
                return redirect('user-post')

            else:
                messages.info(request, "Error! Please check-in only one box")
                return redirect('confirm')

    else:
        form = confirm()

    context = {'form': form,
               'titl': "Confirmation"}
    return render(request, "Seek/confirm.html", context)