from django import forms
from django.core import validators
from django.db.models import fields
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Projects, Review, Profile, REVIEW_CHOICES


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','password1','password2' ] 

        widgets = {
            'first_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"First Name", 'label': 'First Name'}),
            'last_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Second Name", 'label': 'Second Name'}),
            'email':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Email Address", 'label': 'Email Address'}),
            'username':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Username", 'label': 'Username'}),
            'password1':forms.PasswordInput(attrs = {'class':'form-control names','type':'password', 'placeholder':"Password", 'label': 'Password'}),
            'password2':forms.PasswordInput(attrs = {'class':'form-control names', 'placeholder':"Confirm Password", 'label': 'Confirm Password'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio', 'gender', 'phone_number') 

        widgets = {
            'bio': forms.Textarea(attrs={'class':"form-control profile", 'label': 'Bio', 'placeholder':"Bio", 'aria-label':"Bio"}),
            'gender': forms.TextInput(attrs={'class':"form-control profile", 'label': 'Gender', 'placeholder':"Gender", 'aria-label':"Gender"}),
            'phone_number': forms.TextInput(attrs={'class':"form-control profile", 'label': 'Phone Number', 'placeholder':"Phone Number", 'aria-label':"Phone Number"}),
            'profile_photo': forms.FileInput(attrs = {'class': 'form-control photo', 'type': 'file'})
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ('title', 'image', 'description', 'live_link')

        widgets = {
            'title': forms.TextInput(attrs={'class':"form-control project", 'label': 'Title', 'placeholder':"Title", 'aria-label':"Title"}),
            'image': forms.FileInput(attrs = {'class': 'form-control photo', 'type': 'file'}),
            'description' : forms.Textarea(attrs={'class':"form-control project", 'label': 'Description', 'placeholder':"Description", 'aria-label':"Description"}),
            'live_link': forms.URLInput(attrs={'class':"form-control project", 'label': 'Live Link', 'placeholder':"Live Link", 'aria-label':"Live Link"}),
        }
 
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('design', 'usability', 'content')

        widgets = {
            'design': forms.Select(attrs={'class':"form-control review", 'label': 'Design', 'placeholder':"Design", 'aria-label':"Design"}),
            'usability': forms.Select(attrs={'class':"form-control review", 'label': 'Usability', 'placeholder':"Usability", 'aria-label':"Usability"}),
            'content': forms.Select(attrs={'class':"form-control review", 'label': 'Content', 'placeholder':"Content", 'aria-label':"Content"}),
        }