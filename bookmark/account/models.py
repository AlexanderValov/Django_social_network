from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return 'Profile for user {self.user.username}.'

    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo
        else:
            return "https://pbs.twimg.com/media/CIMoiZJW8AE3m-m.jpg"


class Contact(models.Model):
    # ForeignKey на пользователя-подписчика;
    user_form = models.ForeignKey(
        'auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    # ForeignKey на пользователя, на которого подписались;
    user_to = models.ForeignKey(
        'auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    # Менеджеры rel_from_set и  rel_to_set будут возвращать QuerySetʼы модели Contact.
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_form, self.user_to)

# Динамическое добавление поля following в модель User
# Если используется своя модель User, то просто добавить внутрь 
User.add_to_class('following', models.ManyToManyField(
    'self', through=Contact, related_name='followers', symmetrical=False))
