from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *



def index(request):
    """The home page for treaducation"""

    subjects = Subject.objects.order_by('title')

    context = {
        'subjects': subjects,
    }
    
    return render(request, 'courses/index.html', context)

def subject(request, subject_id):
    """show a single subject and its courses
    """

    subject = Subject.objects.get(id=subject_id)
    courses = Course.objects.filter(subject_id = subject_id)
    context = {
        'subject': subject,
        'courses': courses,
    }

    return render(request, 'courses/subject.html', context)

def course(request, course_id):
    """show a single course and its modules
    """

    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(course_id = course_id)
    context = {
        'course': course,
        'modules': modules,
    }

    return render(request, 'courses/course.html', context)

