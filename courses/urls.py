from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # Authentication
    path('login', views.login_user, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.register, name='register'),

    # subjects
    path('subjects/<int:subject_id>/', views.subject, name='subject'),

    # courses
    path('courses/<int:course_id>/', views.course, name='course'),
    path('new_course/<int:user_id>/', views.new_course, name='new_course'),

    # modules
    path('modules/<int:module_id>/', views.module, name='module'),


]