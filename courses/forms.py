from django.contrib.auth.models import User
from django import forms

from .models import Course, Module




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)


class Course_Form(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['subject', 'title', 'overview']
        labels = {
            'subject': 'Subject',
            'title': 'Course Title',
            'overview': 'Course Overview',
        }
       

class Module_Form(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course','title', 'description', 'text', 'image']
        labels = {
            'course': 'Course',
            'title': 'Title',
            'description': 'Description',
            'text': 'Module Text',
            'image': 'Image Content'  
        }