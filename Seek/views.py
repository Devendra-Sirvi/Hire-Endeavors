from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import (RegistrationForm, UserProfileform, UpdateUserProfileform, UserUpdate, OrgRegistrationForm,
                    OrgProfileform, OrgUpdate, OrgProfileUpdate, UserJobPost, OrgJobPost, confirm, consent)
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import org, UserProfile
from jobs.models import userjobpost, orgjobpost
from django.db.models import Q
from django.views.generic.detail import DetailView
# Create your views here.


def index(request):
    data = None
    if request.user.is_authenticated:
        me = request.user.username
        you = f"Welcome {me}, we hope that you discover the best!"
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
            contact = profile.cleaned_data['Contact_Number']
            add = profile.cleaned_data['Residential_Address']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            p = UserProfile.objects.get(user=user)
            p.Contact = contact
            p.Residence = add
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
            add = profile_form.cleaned_data['Site_Address']
            desc = profile_form.cleaned_data['Description']
            contact = profile_form.cleaned_data['Contact_Number']
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = org.objects.get(user=user)
            profile.We_Are = "org"
            profile.orgname = name
            profile.managed_by = mng
            profile.Address = add
            profile.Contact_Number = contact
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
            messages.info(
                request, "Your Post is now streaming, visit \"Posts by Job Seekers\" panel")
            return render(request, "Seek/index.html")

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
            messages.info(
                request, "Your Post is now streaming, visit \"Posts by recruiters\" panel")
            return render(request, "Seek/index.html")
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
    return render(request, "Seek/contact-org.html")


def profile_user(request):
    desc = None
    desc = User.objects.get(username=request.user)
    des = UserProfile.objects.get(user=request.user)
    addr = des.Residence
    addr = "https://www.google.com/maps/place/" + addr
    desc = {'desc': desc, 'des': des, 'addr': addr}
    return render(request, "Seek/users_card.html", desc if desc else None)


def profile_org(request):
    desc = None
    desc = org.objects.get(user=request.user)
    addr = desc.Address
    print(addr)
    addr = "https://www.google.com/maps/place/" + addr
    desc = {'desc': desc, 'des': addr}
    return render(request, "Seek/orgs_card.html", desc if desc else None)


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
            contact = profile_form.cleaned_data['Contact_Number']
            add = profile_form.cleaned_data['Residential_Address']
            profile = UserProfile.objects.get(user=request.user)
            profile.Description = description
            profile.Contact = contact
            profile.Residence = add
            context = {'des': profile, 'addr': add}
            profile.save()
            #profile_form.save()
            messages.success(request, 'Great, User updated successfully!')
            return render(request, 'Seek/users_card.html', context)
    else:
        form = UserUpdate(instance=request.user)
        des = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileform(
            initial={'Description': des.Description, 'Contact_Number': des.Contact, 'Residential_Address': des.Residence})
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
            orgname = profile_form.cleaned_data['Organisation']
            manager = profile_form.cleaned_data['Manager']
            contact = profile_form.cleaned_data['Contact_Number']
            add = profile_form.cleaned_data['Site_Address']
            profile = org.objects.get(user=request.user)
            profile.Description = description
            profile.orgname = orgname
            profile.Contact_Number = contact
            profile.Address = add
            profile.managed_by = manager
            profile.save()
            addr = "https://www.google.com/maps/place/" + add
            #profile_form.save()
            messages.success(request, 'Great, User updated successfully!')
            return render(request, 'Seek/orgs_card.html', {'desc': profile, 'des': addr})
    else:
        form = OrgUpdate(instance=request.user)
        des = org.objects.get(user=request.user)
        profile_form = OrgProfileUpdate(
            initial={'Description': des.Description, 'Organisation': des.orgname, 'Manager': des.managed_by, 'Contact_Number': des.Contact_Number, 'Site_Address': des.Address})
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        args['titl'] = "Org Update"
        return render(request, 'Seek/org_update.html', args)


def post_by_users(request):
    post = userjobpost.objects.all()
    if request.method == 'POST':
        preference = request.POST.get('dosearch')
        post = userjobpost.objects.filter(Q(Description__contains=preference) | Q(Expected_Salary__contains=preference) | Q(
            Position_Name__contains=preference) | Q(Exp__contains=preference) | Q(age__contains=preference))
    con = {'post': post}
    return render(request, "Seek/posts_by_user.html", con)


def post_by_orgs(request):
    post = orgjobpost.objects.all()
    if request.method == 'POST':
        preference = request.POST.get('dosearch')
        post = orgjobpost.objects.filter(Q(Description__contains=preference) | Q(Salary__contains=preference) | Q(
            Position_Name__contains=preference) | Q(Exp__contains=preference) | Q(age__contains=preference) | Q(No_of_openings__contains=preference))
    con = {'post': post}
    return render(request, "Seek/posts_by_org.html", con)


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "Seek/user_card.html"

# class OrgProfileDetailView(DetailView):
#     model = org
#     template_name = "Seek/org_card.html"


class OrgProfileDetailView(DetailView):
    model = org
    template_name = "Seek/contact-org.html"
    
    
def handler_404(request, exception, template_name="Seek/404.html"):
    return render(request, exception, template_name)

def handler_500(request, *args, **argv):
    return render(request, "Seek/500.html")
