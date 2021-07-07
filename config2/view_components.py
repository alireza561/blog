from django.shortcuts import render
from category.models import Category
from repository.repository import category_context
from blog.views import ArticleList


# region main components

def site_header(request):
    return render(request, 'components/site_header.html', category_context())


def site_footer(request):
    return render(request, 'components/site_footer.html', {})


# endregion


# region home components

def home_sliders_components(request):
    return render(request, 'components/home_sliders.html', {})


def latest_blogs_components(request):
    return render(request, 'components/latest_blogs.html', {})


def latest_products_components(request):
    return render(request, 'components/latest_products.html', {})


def best_selling_products_components(request):
    return render(request, 'components/best_selling_products.html', {})


def popular_articles_components(request):
    return render(request, 'components/popular_articles.html', {})


# endregion


# region shop components

# def shop_sidebar_components(request):
#     return render(request, 'components/shop_sidebar.html', {})

# endregion
