from django.contrib.auth import views
from django.urls import path

from account.views import ArticleList, ArticleCreate, ArticleUpdate, UserList, UserUpdate, UserCreate, ArticleDelete, \
    UserDelete, CategoryList, CategoryCreate, CategoryUpdate, CategoryDelete, ArticleTextForAuthor, Profile, Login, \
    PasswordChange, PasswordChangeDone, CommentList

app_name = 'account'

urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('article/create', ArticleCreate.as_view(), name='article-create'),
    path('article/back/<int:pk>', ArticleTextForAuthor.as_view(), name='article-back'),
    path('article/update/<int:pk>', ArticleUpdate.as_view(), name='article-update'),
    path('article/delete/<int:pk>', ArticleDelete.as_view(), name='article-delete'),

    path('users', UserList.as_view(), name='user-list'),
    path('user/create', UserCreate.as_view(), name='user-create'),
    path('user/update/<int:pk>', UserUpdate.as_view(), name='user-update'),
    path('user/delete/<int:pk>', UserDelete.as_view(), name='user-delete'),
    path('profile', Profile.as_view(), name='profile'),

    path('categories', CategoryList.as_view(), name='category-list'),
    path('category/create', CategoryCreate.as_view(), name='category-create'),
    path('category/update/<int:pk>', CategoryUpdate.as_view(), name='category-update'),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name='category-delete'),

    path('comments', CommentList.as_view(), name='comment-list')
]
