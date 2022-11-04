
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login

from .models import Task

#Login view
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
#Register View
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    #If the form is valid then logged the user in & send him to the TaskList
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)   
    
    #If the user is already logged in, send him to the TaskList
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(**args, **kwargs)
        
# All views
# All taks view
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name= 'tasks'
    
    # This method returns the task of the logged in user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)
            
        context['search_input'] = search_input
            
        return context
    
    
# Task detail view
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name= 'task'
    template_name= 'base/task.html'

#Create a new task view
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    #This method takes the logged in user to create his task
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

#Update taks view   
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

#Delete task view
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name= 'task'
    success_url = reverse_lazy('tasks')