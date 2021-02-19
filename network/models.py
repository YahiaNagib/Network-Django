from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from time import strftime
from PIL import Image

class User(AbstractUser):
    followings = models.ManyToManyField("self", related_name="followers", symmetrical=False, blank=True)
    join_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


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