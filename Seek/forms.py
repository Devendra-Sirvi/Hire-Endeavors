from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import org, UserProfile


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='What should we call you?.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='What should be added at the last of your name?.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)

            if commit:
                user.save()
            return user


class OrgRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        exclude = ['first_name', 'last_name']

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)

            if commit:
                user.save()
            return user


class OrgProfileform(forms.Form):
    Organisation = forms.CharField(
        max_length=50, help_text="Organisation name and Username must be same")
    Manager = forms.CharField(
        max_length=50, help_text="Who is managing the company at this portal?")
    Description = forms.CharField(
        max_length=300, help_text="Describe the people you want to hire.")
    Contact_Number = forms.CharField(
        max_length=12, help_text="Inform us your mobile number with country code.")
    Site_Address = forms.CharField(
        max_length=100, help_text="Inform here about where will be the person posted for the Job. (Address of Job posting, with proper descriptive details)")

    class Meta:
        fields = [
            'Organisation',
            'Manager',
            'Description',
        ]


class UserProfileform(forms.Form):
    Description = forms.CharField(
        max_length=300, help_text="Describe yourself and your proffession")

    Contact_Number = forms.CharField(
        max_length=12, help_text="Inform us your mobile number with country code.")
    Residential_Address = forms.CharField(
        max_length=100, help_text="Tell us, what's the place of your residence.")


class OrgJobPost(forms.Form):
    Position_Name = forms.CharField(
        max_length=50, help_text="Job for what position?")
    Description = forms.CharField(
        max_length=150, help_text="Describe the post of Job within 150 words")
    Age_Criteria = forms.IntegerField(
        min_value=18, help_text="(Should be equal or above 18 years)")
    Minimum_required_experience = forms.IntegerField(
        min_value=0, help_text="How much experience do you expect from job seeker?"
    )
    Salary = forms.IntegerField(min_value=0)
    Number_Of_Openings = forms.IntegerField()
    Agree = forms.BooleanField(
        help_text="Checking in this, you confirm that you commit to hire a candidate of age 18 or above and have no obligations to our terms & conditions and privacy policy.")


class UserJobPost(forms.Form):
    Position_Name = forms.CharField(
        max_length=50, help_text="Job for what position?")
    Description = forms.CharField(
        max_length=150, help_text="Describe the job you want within 150 words")
    Expected_Salary = forms.IntegerField(
        help_text="What salary do you expect?")
    Age = forms.IntegerField(
        min_value=18, help_text="What's you age? (Should be equal or above 18 years)")
    Experience = forms.IntegerField(
        min_value=0, help_text="How much you're experienced?"
    )
    Agree = forms.BooleanField(
        help_text="Checking in this, you confirm that your age is 18 or above and have no obligations to our terms & conditions and privacy policy.")


class confirm(forms.Form):
    Want_to_hire = forms.BooleanField(
        help_text="By checking in, You confirm being an organisation and legitely want to hire employees.", required=False)
    Seeking_Jobs = forms.BooleanField(
        help_text="By checking in, You confirm being a legit user want to actively participate in job hiring process by Hire Endeavors.", required=False)


class consent(forms.Form):
    Consent_Code = forms.CharField(
        help_text="Enter <strong>'org'</strong> to confirm you as an organisation or either enter <strong>'seeker'</strong> to inform us that you're a legit job seeker.")

    Agree = forms.BooleanField(
        help_text="We treat you as per your comfortness, please agree and continue.")


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        def __init__(self):
            super(UserUpdate, self).__init__()


class UpdateUserProfileform(forms.Form):
    Description = forms.CharField(max_length=150)
    Contact_Number = forms.CharField(
        max_length=12, help_text="Inform us your mobile number with country code.")
    Residential_Address = forms.CharField(
        max_length=100, help_text="Tell us, what's the place of your residence.")

    class Meta:
        model = UserProfile
        fields = [
            'Description',
        ]

        def __init__(self):
            super(UpdateUserProfileform, self).__init__()


class OrgUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

        def __init__(self):
            super(OrgUpdate, self).__init__()


class OrgProfileUpdate(forms.Form):
    Organisation = forms.CharField(
        max_length=50, help_text="Organisation name and Username must be same")
    Manager = forms.CharField(
        max_length=50, help_text="Who is managing the company at this portal?")
    Description = forms.CharField(
        max_length=300, help_text="Describe the people you want to hire.")
    Contact_Number = forms.CharField(
        max_length=12, help_text="Inform us your mobile number with country code.")
    Site_Address = forms.CharField(
        max_length=100, help_text="Inform here about where will be the person posted for the Job. (Address of Job posting, with proper descriptive details)")
