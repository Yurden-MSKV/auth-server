from decouple import config
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static
from django.utils.text import slugify


def profile_pic_path(instance, filename):
    return f'profiles/{instance.id}/{filename}'


class User(AbstractUser):
    pic = models.ImageField(upload_to=profile_pic_path,
                            null=True,
                            blank=True,
                            verbose_name='Аватарка')
    slug_username = models.SlugField(max_length=30,
                                     unique=True,
                                     blank=True,
                                     verbose_name='slug')
    postfix = models.CharField(max_length=40,
                               blank=True,
                               null=True,
                               verbose_name='Постфикс')
    age = models.PositiveIntegerField(blank=True,
                                      null=True,
                                      verbose_name='Возраст')
    bio = models.TextField(blank=True,
                           null=True,
                           verbose_name='О себе')
    authenticated = models.ManyToManyField('clients.ClientSite',
                                           blank=True,
                                           verbose_name='Профили пользователя')

    def save(self, *args, **kwargs):
        if not self.slug_username:
            self.slug_username = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_pic_url(self):
        if self.pic:
            from django.conf import settings
            if settings.DEBUG:
                return self.pic.url
            else:
                return f'http://{config('CURRENT_IP')}:8000/{self.pic.url}'
        return None

    @property
    def avatar_url(self):
        if self.pic and hasattr(self.pic, "url"):
            return self.pic.url
        return static("images/default_avatar.png")