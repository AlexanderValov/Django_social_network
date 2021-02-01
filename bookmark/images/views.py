from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import redis

from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action


r = redis.Redis(host=settings.REDIS_HOST, 
                        port=settings.REDIS_PORT, 
                        db=settings.REDIS_DB)

@login_required
def images_list(request):
    by_created = '-created'
    by_total_likes = '-total_liks'
    by_title = '-title'
    order_by = request.GET.get('order_by')
    if order_by == None:
        order_by = '-created'
    direction = request.GET.get('direction')
    ordering = order_by
    images = Image.objects.order_by(ordering)
    #images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если переданная страница не является числом, возвращяем первую
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Если получили AJAX-запрос с номером страницы, большим, чем их кол-во
            # возвращаем пустую страницу
            return HttpResponse('')
        # Если номер страницы больше, чем их количество, возвращаем последнюю. 
        images = paginator.page(paginator.num_pages)
    context = {
        'section': 'images',
        'images': images,
        'order_by': order_by,
        'direction': direction,
        'by_created': by_created,
        'by_total_likes': by_total_likes,
        'by_title': by_title
    }
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', context)
    return render(request, 'images/image/list.html', context)

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})

@login_required
def image_create(request):
    if request.method == 'POST':
        # Форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # Добавляем пользователя  созданному объекту
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            messages.success(request, 'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изоброжения
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET-запроса
        form = ImageCreateForm(data=request.GET)

    context = {
        'section': 'images',
        'form': form
    }
    return render(request, 'images/image/create.html', context)


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Увеличиваем количество просмотров картинки на 1
    total_views = r.incr('image:{}:views'.format(image.id))
    # Увеличиваем рейтинг картинки на 1.
    r.zincrby('image_ranking', image.id, 1)
    context = {
        'section': 'images',
        'image': image,
        'total_views': total_views
    }
    return render(request, 'images/image/detail.html', context)

@login_required
def image_ranking(request):
    # Получаем набор рейтинга картинок
    image_ranking = r.zrange('image_ranking', 0, 1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # Получаем отсортированый список самых популярный картинок
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    context = {
        'section': 'images',
        'most_viewed': most_viewed
    }
    return render(request, 'images/image/ranking.html', context)