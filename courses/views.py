from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *



def index(request):
    """The home page for treaducation"""

    subject_list = Subject.objects.order_by('title')

    context = {
        'subject_list': subject_list,

    }
    
    return render(request, 'courses/index.html', context)
