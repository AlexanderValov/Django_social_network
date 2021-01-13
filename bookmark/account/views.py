from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_form=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(
                    user_form=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


@login_required
def user_list(request):
    users_all = User.objects.filter(is_active=True)
    paginator = Paginator(users_all, 10)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {
        'section': 'people',
        'users': users,
        'page': page,
    }
    return render(request, 'account/user/list.html', context)


@login_required
def user_detail(request, username):
    # получение активного пользователя по его логину
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'peolpe', 'user': user})


@login_required
def edit(request):
    # Изменение профиля
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
    # По умолчанию отображаем все действия
    # Кроме авторизованного пользователя
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # Если пользователь подписался на кого, показывает только его активность
        actions = actions.filter(user_id__in=following_ids)
    # Метод select_related() помогает нам оптимизировать доступ к объектам,
    # связанным отношением «один ко многим»
    actions = actions.select_related(
        'user', 'user__profile').prefetch_related('target')[:10]
    # метод prefetch_related() работает для отношений «многие ко многим» и
    # «многие к одному» (ManyToMany и обратная связь для ForeignKey).
    # и к полям типов GenericRelation и GenericForeignKey.
    paginator = Paginator(actions, 5)
    page = request.GET.get('page')
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)
    context = {
        'section': 'dashboard',
        'actions': actions
    }
    return render(request, 'account/dashboard.html', context)

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
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})
