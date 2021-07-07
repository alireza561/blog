from django.contrib import admin, messages
from django.utils.translation import ngettext
from .models import Article, IPAddress

# region admin header change
admin.site.site_header = 'وبلاگ جنگویی من'


# endregion
# Register your models here.

def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d مقاله منتشر شد.',
        '%d مقاله منتشر شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_published.short_description = 'انتشار مقالات انتخاب شده'


def make_draft(modeladmin, request, queryset):
    # queryset.update(status='d')
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d مقاله پیش نویس شد.',
        '%d مقاله پیش نویس شدند.',
        updated,
    ) % updated, messages.SUCCESS)


make_draft.short_description = 'پیش نویس شدن مقالات انتخاب شده'


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'thumbnail_tag', 'category_to_str', 'slug', 'jpublish', 'is_special', 'status')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
admin.site.register(IPAddress)
