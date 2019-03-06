from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError
from django.template import RequestContext
from django.shortcuts import render
from django.urls import reverse

from courses.forms import *
from .models import *


# Homepage =========================================
def index(request):
    """The home page for treaducation"""

    subjects = Subject.objects.order_by('title')

    context = {
        'subjects': subjects,
    }
    
    return render(request, 'courses/index.html', context)

# End Homepage ======================================

# Authentication ====================================

def register(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        return login_user(request)

    elif request.method == 'GET':
        user_form = UserForm()
        template_name = 'registration/register.html'
        return render(request, template_name, {'user_form': user_form})


def login_user(request):
    '''Handles the creation of a new user for authentication
    Method arguments:
      request -- The full HTTP request object
    '''

    # Obtain the context for the user's request.
    context = {'next': request.GET.get('next', '/')}
    print("CONTEXT:", context)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        username=request.POST['username']
        password=request.POST['password']
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, log the user in
        if authenticated_user is not None:
            login(request=request, user=authenticated_user)
            if request.POST.get('next') == '/':
              return HttpResponseRedirect('/')
            else:
              print("ELSE STATEMENT:", request.POST.get('next', '/'))
              return HttpResponseRedirect(request.POST.get('next', '/'))

        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")


    return render(request, 'registration/login.html', context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage. Is there a way to not hard code
    # in the URL in redirects?????
    return HttpResponseRedirect('/')

# End Authentication ================================


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

