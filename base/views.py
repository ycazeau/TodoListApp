
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from .models import Task

#Login view
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    

# All views
# All taks view
class TaskList(ListView):
    model = Task
    context_object_name= 'tasks'
    
# Task detail view
class TaskDetail(DetailView):
    model = Task
    context_object_name= 'task'
    template_name= 'base/task.html'

#Create a new task view
class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

#Update taks view   
class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')

#Delete task view
class TaskDelete(DeleteView):
    model = Task
    context_object_name= 'task'
    success_url = reverse_lazy('tasks')