from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ValidationError
from django.template import RequestContext
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.urls import reverse
from django.db.models import Count
from django.views.generic.detail import DetailView
from django.contrib import messages


from courses.forms import *
from .models import *


# Homepage =========================================
def index(request, subject=None):
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
    return render(request, 'registration/logged_out.html')

# End Authentication ================================

# Subjects ==========================================
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

# End Subjects =======================================

# Courses ============================================

def course(request, course_id):
    """show a single course and its modules
    """

    course = Course.objects.get(id=course_id)
    modules = Module.objects.filter(course_id = course_id)
    subject = course.subject
    context = {
        'course': course,
        'modules': modules,
        'subject': subject,
    }

    return render(request, 'courses/course.html', context)

# ***Instructor methods***

@login_required
def new_course(request, user_id):
    ''' adds new courses to treaducation
    '''
    user = User.objects.get(id=user_id)
    subject = Subject.objects.order_by('title')

    if request.method != 'POST':
      form = CourseForm()
    else:
      form = CourseForm(data=request.POST)
      if form.is_valid():
          form.save()
          return HttpResponseRedirect(reverse('courses:my_courses'))

    context = {
        'user': user,
        'form': form,
        'subject': subject}
    return render(request, 'courses/new_course.html', context)


@login_required
def my_courses(request):
    '''Show all courses created by user'''

    template_name = 'courses/my_courses.html'
    courses = Course.objects.filter(owner=request.user)
    context = {
        'courses': courses,
    }

    return render(request, template_name, context)

@login_required
def my_course_detail(request, course_id):
    """Show a single course and all of its modules."""

    course = Course.objects.get(id=course_id)
    modules = course.module_set.order_by('title')
    context = {'course': course, 'modules': modules}

    return render(request, 'courses/my_course_detail.html', context)


@login_required
def course_delete(request, course_id):
    '''delete course from course list'''

    course = Course.objects.get(id=course_id)
    courses = Course.objects.filter(owner=request.user).order_by('title')

    course.delete()
    messages.success(request, 'Your course has been deleted!')
    return HttpResponseRedirect(reverse('courses:my_courses'))

    context = {'courses': courses}
    return render(request, 'courses/course_delete.html', context)


@login_required
def course_edit(request, course_id):
    """Edit an existing course"""

    course = Course.objects.get(id=course_id)
    courses = Course.objects.filter(owner=request.user)


    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = CourseForm(instance=course)
    else:
        form = CourseForm(instance=course, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('courses:my_courses'))

    context = {'course': course, 'courses': courses, 'form': form}
    return render(request, 'courses/edit_course.html', context)

# End Courses ========================================

# Modules ============================================

def module(request, module_id):
    """show a single module and its contents
    """

    module = Module.objects.get(id=module_id)
    course = module.course
    context = {
        'module': module,
        'course': course,
    }

    return render(request, 'courses/module.html', context)

# ***Instructor methods***

@login_required
def new_module(request, course_id):
    ''' adds new modules to treaducation
    '''
    course = Course.objects.get(id=course_id)

    if request.method != 'POST':
      form = ModuleForm()
    else:
      form = ModuleForm(request.POST, request.FILES)
      if form.is_valid():
          new_module = form.save(commit=False)
          new_module.course = course
          new_module.save()
          return HttpResponseRedirect(reverse('courses:my_course_detail', args=[course_id]))
    context = {
        'form': form,
        'course': course}
    return render(request, 'courses/new_module.html', context)

@login_required
def module_delete(request, module_id):
    '''delete module from module list'''

    module = Module.objects.get(id=module_id)
    course = module.course

    module.delete()
    messages.success(request, 'Your module has been deleted!')
    return HttpResponseRedirect(reverse('courses:my_course_detail', args=[course.id]))

    context = {'module': module, 'course': course}
    return render(request, 'courses/my_course_detail.html', context)

@login_required
def module_edit(request, module_id):
    """Edit an existing module."""

    module = Module.objects.get(id=module_id)
    course = module.course

    if request.method != 'POST':
        #Initial request; pre-fill form with the current entry.
        form = ModuleForm(instance=module)
    else:
        #POST data submitted; process data.
        form = ModuleForm(instance=module, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('courses:my_course_detail', args=[course.id]))

    context = {'module': module, 'course': course, 'form': form}
    return render(request, 'courses/module_edit.html', context)


# End Modules ==========================================

# Student Enrollment ===================================

def student_enroll(request, course_id):
    """add student to course enrollment
    """
    student = User.objects.get(id=request.user.id)
    enrolled_course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        # creates new join table record with current user and selected course
        new_student = CourseStudent(
            student = student,
            course = enrolled_course,
        )

        new_student.save()

    return HttpResponseRedirect(reverse('courses:enroll_list'))

def enroll_list(request):
    """lists the courses in which the request student has enrolled 
    """

    courses = CourseStudent.objects.filter(student = request.user)
    course_enrollments = courses
    context = {
        'course_enrollments':course_enrollments,
    }

    return render(request, 'courses/student_courses.html', context)








# End Student Enrollment ===============================




