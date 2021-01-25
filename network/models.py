from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from time import strftime

class User(AbstractUser):
    followings = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)
    join_date = models.DateTimeField(default=timezone.now)

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="liked_post")

    def __str__(self):
        return f'{self.user.username} post on {self.date.strftime("%m/%d/%Y")}'

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="comments",on_delete=models.CASCADE )
    user = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)