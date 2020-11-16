"""Todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from todo_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #Auth
    path('signup/', views.signupuser,name="signupuser"),
    path('logout/', views.logoutuser, name="logout"),
    path('login/', views.loginuser, name="login" ),

    #current_todos
    path('', views.home, name='home'),
    path('yourtodos/', views.current_todos, name="current_todos"),
    path('create/', views.create_todos, name='todos'),
    path('todo/<int:todos_pk>', views.viewtodo, name="viewtodo"),
    path('todo/<int:todos_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todos_pk>/delete', views.deletetodo, name='deletetodo'),
    path('completed/', views.list_completed, name="list_completed"),
]
