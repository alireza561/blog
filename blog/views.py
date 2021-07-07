from django.db.models import Count, Q

from account.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article
from account.mixins import AuthorAccessMixin
from datetime import datetime, timedelta
from category.models import Category
from django.core.paginator import Paginator


# from django.http import HttpResponse


# Create your views here.


# def blog_detail(request, slug):
#     context = {
#         'article': get_object_or_404(Article.objects.published(), slug=slug)
#     }
#     return render(request, 'blog/article_detail.html', context)


# def blog_list(request):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 2)
#     page = request.GET.get('page')
#     articles = paginator.get_page(page)
#     context = {
#         'articles': articles,
#         'page_title': 'مقالات'
#     }
#     return render(request, 'blog/article_list.html', context)

class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 2

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     last_month = datetime.today() - timedelta(days=30)
    #     context['popular_articles'] = Article.objects.published().annotate(
    #         count=Count('hits', filter=Q(articlehit__created__gt=last_month))
    #     ).order_by('-count', '-publish')[:3]
    #     return context

    # ====== for example  Q object =====  (__gt, __year, __month)  is query (is lookup in the google(django lookup))
    # Q(articlehit__created__year=2020)
    # Q(articlehit__created__month=12)
    # Q(articlehit__created__year=2020) | Q(articlehit__created__month=12)
    # Q(articlehit__created__year=2020) & Q(articlehit__created__month=12)


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class AuthorList(ListView):
    paginate_by = 2
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
