from django.db import models
from django.urls import reverse
from django.conf import settings
# работает для русского и английского алфавита
from pytils.translit import slugify


# Эта модель будет использована для сохранения изображений, добавленных
# в закладки.
class Image(models.Model):
    # user – указывает пользователя, который добавляет изображение в  закладки.
    # Это поле является внешним ключом и использует связь «один ко многим».
    # Пользователь может сохранять много изображений, но каждая картинка
    # может быть сохранена только одним пользователем.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)
    # Аргумент db_index=True говорит Django о необходимости создать индекс по этому полю.
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])
