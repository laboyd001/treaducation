from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    # Homepage
    # ==================================================
    path('', views.index, name='index'),

    # Authentication
    # ==================================================
    path('login', views.login_user, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.register, name='register'),

    # subjects
    # ==================================================
    path('subjects/<int:subject_id>/', views.subject, name='subject'),

    # courses
    # ==================================================
    path('courses/<int:course_id>/', views.course, name='course'),
    

    # modules
    # ==================================================
    path('modules/<int:module_id>/', views.module, name='module'),

    # instructor urls
    # ==================================================
    # add courses
    path('new_course/<int:user_id>/', views.new_course,name='new_course'),
    # add modules
    path('new_module/<int:course_id>/', views.new_module,name='new_module'),
    # view your courses
    path('my_courses/', views.my_courses,name='my_courses'),
    # view the details of your course
    path('my_courses/detail/<int:course_id>/', views.my_course_detail,name='my_course_detail'),
    # delete a course
    path('my_courses/delete/<int:course_id>',views.course_delete, name='course_delete'),
    #  edit a course
    path('my_courses/edit/<int:course_id>',views.course_edit, name='course_edit'),


]
