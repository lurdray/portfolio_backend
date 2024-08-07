
from django.urls import path 
from . import views 

app_name = "project"

urlpatterns = [

    path('project/', views.project_list, name = 'project_list'), 
    path('project/<str:pk>/', views.project_detail, name = 'project_detail'),


]

