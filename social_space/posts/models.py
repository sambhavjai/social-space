from django.db import models
from django.conf import settings
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from groups.models import Group
import misaka

class Post(models.Model):
    user = models.ForeignKey(User,related_name='posts',on_delete=models.DO_NOTHING)
    create_date = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta():
        ordering = ['-create_date']
        unique_together = ('user','message')
