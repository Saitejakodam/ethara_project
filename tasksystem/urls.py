from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('create-project/', views.create_project),
    path('project/<int:project_id>/', views.project_details),
    path('project/<int:project_id>/create-task/', views.create_task),
    path('mytasks/', views.my_tasks),
    path('edit-task/<int:task_id>/', views.edit_task),
]