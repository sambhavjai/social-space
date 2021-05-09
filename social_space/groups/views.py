from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView,DetailView,ListView
from .models import Group,GroupMember

class CreateGroup(CreateView,LoginRequiredMixin):
    fields = ('name','description')
    model = Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group
