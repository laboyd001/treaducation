from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *



def index(request):
    """The home page for treaducation"""
    
    return render(request, 'courses/index.html')
