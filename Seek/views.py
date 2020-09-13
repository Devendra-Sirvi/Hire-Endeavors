from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import (RegistrationForm, UserProfileform, UpdateUserProfileform, UserUpdate, OrgRegistrationForm,
                    OrgProfileform, OrgUpdate, OrgProfileUpdate, UserJobPost, OrgJobPost, confirm, consent)
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import org, UserProfile
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
        profile = UserProfileform(request.POST)

        if form.is_valid() and profile.is_valid():
            form.save()
            p = UserProfile()
            desc = profile.cleaned_data['Description']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            prof = UserProfile()
            prof.user = user
            prof.save()
            p = UserProfile.objects.get(user=user)
            p.Description = desc
            p.save()

            login(request, user)
            return redirect('index')
    else:
        # form = RegistrationForm()
        form = RegistrationForm()
        profile = UserProfileform()

    context = {'form': form, 'profile': profile, 'titl': "User Sign-up"}
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

    context = {'form': form, 'titl': "Request Job Post",
               'act': "/create-user-post/"}
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

    context = {'form': form, 'titl': "Publish Job Post",
               'act': "/create-org-post/"}
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


def card(request):
    return render(request, "Seek/card.html")


def profile_user(request):
    desc = None
    desc = User.objects.get(username=request.user)
    des = UserProfile.objects.get(user=request.user)
    desc = {'desc': desc, 'des': des}
    return render(request, "Seek/user_card.html", desc if desc else None)


def profile_org(request):
    desc = None
    desc = org.objects.get(user=request.user)
    desc = {'desc': desc}
    return render(request, "Seek/org_card.html", desc if desc else None)


def clientconsent(request):
    if request.method == "POST":
        form = consent(request.POST)

        if form.is_valid():
            code = form.cleaned_data['Consent_Code']
            if(code == "org"):
                return redirect('org-profile')

            else:
                #messages.info(request, "Error! Please check-in only one box")
                return redirect('user-profile')

    else:
        form = consent()

    context = {'form': form,
               'titl': "Consent"}
    return render(request, "Seek/consent.html", context)


def UserUpdatation(request):
    if request.method == 'POST':
        form = UserUpdate(request.POST, instance=request.user)
        profile_form = UpdateUserProfileform(request.POST)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            description = profile_form.cleaned_data['Description']
            profile = UserProfile.objects.get(user=request.user)
            profile.Description = description
            profile.save()
            #profile_form.save()
            messages.success(request, 'Great, User updated successfully!')
            return render(request, 'Seek/user_card.html', {'des': profile})
    else:
        form = UserUpdate(instance=request.user)
        des = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileform(
            initial={'Description': des.Description})
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        args['titl'] = "User Update"
        return render(request, 'Seek/user_update.html', args)


def OrgUpdatation(request):
    if request.method == 'POST':
        form = OrgUpdate(request.POST, instance=request.user)
        profile_form = OrgProfileUpdate(request.POST)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            description = profile_form.cleaned_data['Description']
            orgname = profile_form.cleaned_data['orgname']
            manager = profile_form.cleaned_data['managed_by']
            profile = org.objects.get(user=request.user)
            profile.Description = description
            profile.orgname = orgname
            profile.managed_by = manager
            profile.save()
            #profile_form.save()
            messages.success(request, 'Great, User updated successfully!')
            return render(request, 'Seek/org_card.html', {'desc': profile})
    else:
        form = OrgUpdate(instance=request.user)
        des = org.objects.get(user=request.user)
        profile_form = OrgProfileUpdate(
            initial={'Description': des.Description, 'orgname': des.orgname, 'managed_by': des.managed_by})
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        args['titl'] = "Org Update"
        return render(request, 'Seek/org_update.html', args)


def post_by_users(request):
    post = userjobpost.objects.all()
    con = {'post': post}
    return render(request, "Seek/posts_by_user.html", con)


def post_by_orgs(request):
    post = orgjobpost.objects.all()
    con = {'post': post}
    return render(request, "Seek/posts_by_org.html", con)
