from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView,DetailView,ListView,RedirectView
from django.contrib import messages

from .models import Group,GroupMember

class CreateGroup(CreateView,LoginRequiredMixin):
    fields = ('name','description')
    model = Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group

class JoinGroup(RedirectView,LoginRequiredMixin):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Already a member!')
        else:
            messages.success(self.request,'Added to the group')

        return super().get(request,*args,**kwargs)

class LeaveGroup(RedirectView,LoginRequiredMixin):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):

        try:
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,'You are not a member of this group')
        else:
            membership.delete()
            messages.success(self.request,'Group membership deleted')

        return super().get(request,*args,**kwargs)
