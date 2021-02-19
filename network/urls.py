
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("save-post", views.save_post, name="save-post"),
    path("edit-post", views.edit_post, name="edit-post"),

    path("profile/<int:id>", views.profile_view, name="profile"),
    path("follow/<int:id>", views.follow_user, name="follow"),
    path("following", views.following_posts, name="following-posts"),
    path("like", views.like_post, name="like-post"),

    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("edit-profile", views.edit_profile, name="edit-profile"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)