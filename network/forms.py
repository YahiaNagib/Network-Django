from django import forms
from django.forms import ModelForm
from .models import Post, User


class AddPost(ModelForm):

    class Meta:
        model = Post
        fields = ['content']


class UserUpdateForm(ModelForm):

    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg mb-2'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-lg mb-2'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control-file mb-3'}),
        }
        fields = ['username', 'email', 'image']