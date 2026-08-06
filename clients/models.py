from django.db import models

class ClientSite(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name='Название')
    link = models.URLField(max_length=200,
                           unique=True,
                           verbose_name='Ссылка для правок')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Актив')

    def __str__(self):
        return self.name