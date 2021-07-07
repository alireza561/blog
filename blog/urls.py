from django.urls import path
from .views import ArticleDetail, ArticleList, AuthorList, ArticlePreview

app_name = "blog"
urlpatterns = [
    path('article-list', ArticleList.as_view(), name='article_list'),
    path('article/<slug:slug>', ArticleDetail.as_view(), name='article'),
    path('preview/<int:pk>', ArticlePreview.as_view(), name='preview'),
    path('author/<slug:username>', AuthorList.as_view(), name='author')
]
