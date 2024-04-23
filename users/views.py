from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm, PostForm
from django.http import HttpResponseRedirect


# menu = [
#         {'title': "Авторизация", 'url_name': 'login'},
#         {'title': "Регистрация", 'url_name': 'register'},
# ]


def index(request):
    data = {
        'title': 'Главная страница',
        # 'menu': menu,
    }
    return render(request, 'users/index.html', context=data)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    data = {
        # 'menu': menu,
        'form': form,
    }
    return render(request, 'users/register.html', context=data)


@login_required
def profile(request):
    data = {
        # 'menu': menu,
        'user': request.user,
    }
    return render(request, 'users/profile.html', context=data)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            form = ProfileForm(instance=request.user.profile)
        return render(request, 'users/edit_profile.html', {'form': form})
    else:
        form = ProfileForm(instance=request.user.profile)
        return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile')
        else:
            form = PostForm()
        return render(request, 'users/create_post.html', {'form': form})
    else:
        form = PostForm(request.POST)
        return render(request, 'users/create_post.html', {'form': form})