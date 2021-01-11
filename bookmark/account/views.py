from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        try:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        except ObjectDoesNotExist:
            Profile.objects.create(user=request.user)
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context)


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def user_login(request):
    if request.method == 'POST':
        # Когда пользователь отправляет форму POST-запросом, мы обрабатываем ее:
        form = LoginForm(request.POST)  # создаем объект формы с данными
        if form.is_valid():  # проверяем, правильно ли заполнена форма = продолжение либо ошибка
            cd = form.cleaned_data
            # если данные введены верно, сверяем их с данными в базе с помощью
            # функции authenticate().
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            # authenticate() принимает аргументы request, username и password
            # и возвращает объект пользователя User, если он успешно аутентифицирован.
            # В противном случае вернется None. Если пользователь не был аутентифицирован,
            #  возвращаем объект HttpResponse с  сообщением о некорректном логине или пароле;
        if user is not None:
            if user.is_active:
                # если пользователь активный, авторизуем его на сайте.
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disable account')
        else:
            return HttpResponse('Invalid login')
    else:
        # Когда user_login вызывается с GET-запросом, мы создаем новую форму логина выражением
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Когда пользователь регистрируется на сайте, мы создаем пустой профиль, 
            # ассоциированный с ним
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
