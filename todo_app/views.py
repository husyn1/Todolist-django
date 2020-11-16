from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todos
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "todo_app/home.html")

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo_app/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current_todos')
            except IntegrityError:
                return render(request, 'todo_app/signupuser.html',{'form':UserCreationForm() , "error" : " This username is already taken. Please try a different username!"})
        else:
            return render(request, 'todo_app/signupuser.html',{'form':UserCreationForm(), "error" :" passwords didn't match"})

@login_required
def current_todos(request):
    todos=Todos.objects.filter(user=request.user,datecompleted__isnull=True )
    return render(request, "todo_app/currentodo.html", {'todo':todos})

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home") 

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo_app/loginuser.html',{'form':AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo_app/loginuser.html',{'form':AuthenticationForm(), "error": "Username and password did not match"})
        else:
            login(request, user)
            return redirect("current_todos")

@login_required
def create_todos(request):
    if request.method == "GET":
        return render(request, 'todo_app/todos.html',{'form':TodoForm})

    else:
        try:
            form = TodoForm(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo_app/todos.html', {'form':TodoForm(), "error":"bad data passed in. please try again"})

@login_required
def viewtodo(request, todos_pk):
    todo=get_object_or_404(Todos, pk=todos_pk, user=request.user)
    if request.method=='GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo_app/viewtodos.html', {'todo':todo , 'form':form})
    else:
        try: 
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect("current_todos")
        except ValueError:
            return render(request, 'todo_app/viewtodos.html', {'todo':todo , 'form':form, "error":"bad data passed in"})

@login_required
def completetodo(request, todos_pk):
    todo=get_object_or_404(Todos,pk=todos_pk, user=request.user)
    if request.method=='POST':
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect("current_todos")

@login_required
def deletetodo(request, todos_pk):
    todo=get_object_or_404(Todos,pk=todos_pk, user=request.user)
    if request.method=='POST':
        todo.delete()
        return redirect("current_todos")

@login_required
def list_completed(request):
    todos=Todos.objects.filter(user=request.user,datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, "todo_app/listcompleted.html", {'todo':todos})

         
