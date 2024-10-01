from . import views
from django.urls import path

urlpatterns = [
    path("hello", views.index, name="hello"),
    path("signup", views.createUser, name='signup'),
    path("login", views.login, name='login'),
    path("createTask", views.create_task, name='create_task'),
    path("getTasks", views.get_tasks, name='get_tasks'),
    path("getUser", views.getUser, name='getUser'),
    path("updateTask", views.update_tasks, name='update_tasks'),
    path("deltask", views.delete_task, name='delete_task'),
    path("updateUser", views.updateAccount, name='updateAccount'),
]