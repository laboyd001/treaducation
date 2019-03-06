from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

]