from django.urls import path
from .views import TaskApiView, TaskDetailApiView

urlpatterns = [
    path('tasks/', TaskApiView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailApiView.as_view(), name='task-detail'),
]