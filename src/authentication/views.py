from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from . import models
from . import forms


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = models.UserCustom.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('feed:home')
        else:
            messages.error(request, 'Username OR password does not exit')
    return render(request, 'authentication/login_page.html')


@login_required
def logout_page(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


@login_required
def follow_page(request):
    user_to_follow = models.UserCustom.objects.all().exclude(id=request.user.id)
    if request.method == "POST":
        user_search = request.POST.get("follow_user")
        if user_search == request.user.username:
            messages.error(request, 'You cannot follow yourself')
        else:
            try:
                following_user = models.UserCustom.objects.get(username=user_search)

                if models.UserFollows.objects.filter(user=request.user, followed_user=following_user).exists():
                    messages.error(request, "Vous suivez déjà cet utilisateur.")
                else:
                    models.UserFollows.objects.create(user=request.user, followed_user=following_user)
                    messages.success(request, f"Vous suivez maintenant {following_user.username}.")

            except models.UserCustom.DoesNotExist:
                messages.error(request, "Utilisateur inconnu.")

    following_user = models.UserCustom.objects.filter(followed_by__user=request.user)
    followers = models.UserCustom.objects.filter(following__followed_user=request.user)
    print(followers)
    return render(request, 'authentication/follow_page.html', {'user_to_follow': user_to_follow,
                                                               'following_user': following_user,
                                                               'following_me': followers})


@login_required
def unfollow_user(request, user_to_unfollow):
    user_to_unfollow = get_object_or_404(models.UserCustom, id=user_to_unfollow)
    follow_relation = models.UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).first()

    if follow_relation:
        follow_relation.delete()
        messages.success(request, f"Vous avez arrêté de suivre {user_to_unfollow.username}.")
    else:
        messages.error(request, "Vous ne suivez pas cet utilisateur.")

    return redirect("auth:follow")


def create_account(request):
    forms_page = forms.CreateUserForm()
    if request.method == "POST":
        forms_page = forms.CreateUserForm(request.POST)
        if forms_page.is_valid():
            user = forms_page.save()
            print(user)
            login(request, user)
            return redirect('feed:home')
    return render(request, 'authentication/register.html', {'forms_page': forms_page})
