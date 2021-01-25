from django import forms
from django.forms import ModelForm
from .models import Post


class AddPost(ModelForm):

    class Meta:
        model = Post
        fields = ['content']