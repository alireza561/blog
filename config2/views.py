from django.shortcuts import render

from category.models import Category


def home(request):
    context = {
        'page_title': 'صفحه اصلی'
    }
    return render(request, 'pages/home.html', context)
