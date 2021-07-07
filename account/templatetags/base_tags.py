from datetime import datetime, timedelta

from django import template
from django.db.models import Count, Q

from blog.models import Article

register = template.Library()


@register.inclusion_tag('registration/partials/sidebar_active.html')
def link(request, link_name, content):
    return {
        'request': request,
        'link_name': link_name,
        'link': 'account:{}'.format(link_name),
        'content': content
    }


@register.inclusion_tag('blog/partials/popular_articles.html')
def popular_articles():
    last_month = datetime.today() - timedelta(days=30)
    return {
        'popular_articles': Article.objects.published().annotate(
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))
        ).order_by('-count', '-publish')[:3]
    }

# @register.simple_tag
# def title():
#     return 'فروشگاه مرکزی'

# @register.inclusion_tag('components/partials/category_navbar.html')
# def category_navbar():
#     return {
#         'category': Category.objects.filter(status=True)
#     }
