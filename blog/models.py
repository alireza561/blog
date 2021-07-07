from account.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from extensions.utils import jalali_converter
from category.models import Category
from django.utils.html import format_html

# import library for comment
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# region IPAddress =====================================================================

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')

    class Meta:
        verbose_name = 'آدرس آی پی'
        verbose_name_plural = 'آدرس آی پی'

# endregion


# region Article =============================================================================


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # publish
        ('i', 'درحال بررسی'),  # investigation
        ('b', 'برگشت داده شده')  # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles',
                               verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='آدرس مقاله')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    description = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to="images", verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    TextForAuthor = models.TextField(default=None, null=True, blank=True, verbose_name='دلیل برگشت')
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, blank=True, through='ArticleHit', related_name='hits',
                                  verbose_name='بازدیدها')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)

    jpublish.short_description = "زمان انتشار"

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius:5px;' src='{}'>".format(self.thumbnail.url))

    thumbnail_tag.short_description = "تصویر"

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])

    category_to_str.short_description = 'دسته بندی'

    def get_absolute_url(self):
        return reverse('account:home')

    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

# endregion
