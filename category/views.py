from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from blog.models import Article
from category.models import Category


# def category(request, slug):
#     category = get_object_or_404(Category.objects.active(), slug=slug)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 2)
#     page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         'category': category,
#         'articles': articles
#
#     }
#     return render(request, 'category/category_list.html', context)


class CategoryList(ListView):
    template_name = 'category/category_list.html'
    paginate_by = 2

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
