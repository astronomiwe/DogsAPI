from django.db import models
from django.utils.timezone import now


class Feedback(models.Model):
    """заводчик"""
    id = models.AutoField
    name = models.CharField(max_length=200, verbose_name='имя отправителя', null=False)
    email = models.EmailField(verbose_name='контактный е-майл', null=False)
    message = models.TextField(verbose_name='сообщение', null=False)
    created_at = models.DateTimeField(default=now, verbose_name='время отправки')
