import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Comment
from .forms import UserUpdateForm


def index(request):
    
    posts = Post.objects.all().order_by("-date")
    p = Paginator(posts, 10)

    if request.GET.get("page"):
        current_page = int(request.GET.get("page"))
    else:
        current_page = 1

    context = {
        "posts": p.page(current_page).object_list,
        "pages_count": range(1, p.num_pages + 1),
        "total_pages": p.num_pages,
        "current_page": current_page,
        "main_page": True,
    }
    return render(request, "network/index.html", context)


@login_required
def save_post(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            # if post-id exists which means to edit the post
            content = request.POST["content"]
            new_post = Post(content=content, user=request.user)
            new_post.save()
            messages.success(request, "Your post has been added")
            return redirect("index")
        else:
            return redirect("login")


@login_required
def edit_post(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            if "postId" in data:

                id = data["postId"]
                content = data["content"]
                post = Post.objects.filter(id=id).first()
                if request.user != post.user:
                    messages.error(request, "Forbidden, you can not edit this post")
                    return redirect("index")

                post.content = content
                post.save()
                return JsonResponse({"message": content}, status=201)
        else:
            return redirect("login")


@login_required
def profile_view(request, id):

    user = User.objects.filter(id=id).first()

    if user == None:
        messages.error(request, "This user does not exist")
        return redirect("index")

    # if the authenticated user is following the user whose page is opened
    # then is_follow is True to make the unfollow button appear
    if request.user in user.followers.all():
        is_follow = True
    else:
        is_follow = False

    posts = user.posts.all().order_by("-date")
    p = Paginator(posts, 10)

    if request.GET.get("page"):
        current_page = int(request.GET.get("page"))
    else:
        current_page = 1

    context = {
        "posts": p.page(current_page).object_list,
        "pages_count": range(1, p.num_pages + 1),
        "total_pages": p.num_pages,
        "current_page": current_page,
        "followings": user.followings.all().count(),
        "followers": user.followers.all().count(),
        "required_user": user,
        "name": user.username,
        "id": user.id,
        "is_follow": is_follow,
    }

    return render(request, "network/profile.html", context)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        form.save()
        messages.success(request, f'Your account has been updated!')
        return redirect('index')

    form = UserUpdateForm(instance=request.user)
    return render(request, "network/edit-profile.html", {'form': form})

@login_required
def follow_user(request, id):
    if request.method == "POST":
        user = User.objects.filter(id=id).first()
        # ensure that the user is not following themselves
        if user != request.user:
            # if the user is not followed by the authenticated user
            if user not in request.user.followings.all():
                request.user.followings.add(user)
                request.user.save()
                return redirect("profile", id)
            else:
                request.user.followings.remove(user)
                request.user.save()
                return redirect("profile", id)


@login_required
def following_posts(request):
    followed_users = request.user.followings.all()
    follow_posts = []

    for user in followed_users:
        for post in user.posts.all().order_by("-date"):
            follow_posts.append(post)

    p = Paginator(follow_posts, 10)

    if request.GET.get("page"):
        current_page = int(request.GET.get("page"))
    else:
        current_page = 1

    context = {
        "posts": p.page(current_page).object_list,
        "pages_count": range(1, p.num_pages + 1),
        "total_pages": p.num_pages,
        "current_page": current_page,
        "main_page": False,
    }

    # context = {
    #     "posts": follow_posts,
    #      "main_page": False
    # }
    return render(request, "network/index.html", context)


@login_required
def like_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if "postId" in data:
            id = data["postId"]
            post = Post.objects.filter(id=id).first()
            if request.user not in post.likes.all():
                post.likes.add(request.user)
                post.save()
            else:
                post.likes.remove(request.user)
                post.save()

            likes_number = post.likes.all().count()
            return JsonResponse({"message": likes_number}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
