from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # subjects
    path('subjects/<int:subject_id>/', views.subject, name='subject'),

]