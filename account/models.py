from django.urls import reverse
from django.utils import timezone

from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    is_author = models.BooleanField(default=False, verbose_name='وضعیت نویسندگی')
    special_user = models.DateTimeField(default=timezone.now, verbose_name='کاربر ویژه تا')

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    is_special_user.boolean = True
    is_special_user.short_description = 'کاربر ویژه'

    def get_absolute_url(self):
        return reverse('account:user-list')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-is_superuser', '-is_staff', '-is_author', '-special_user']
