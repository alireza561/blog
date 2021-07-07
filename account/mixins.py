from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from blog.models import Article


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['title', 'slug', 'category', 'description', 'thumbnail', 'publish', 'status', 'is_special']
        if request.user.is_superuser:
            self.fields += 'author', 'TextForAuthor'

        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'

        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['d', 'b'] \
                or request.user.is_superuser:
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            return redirect('account:home')


class ArticleBackAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if article.status == 'b':
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            return redirect('account:home')


class UserFieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_author',
                       'special_user', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined']

        return super().dispatch(request, *args, **kwargs)


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')


class AdminUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_author or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')


class CategoryFieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = ['parent', 'title', 'slug', 'status', 'position']

        return super().dispatch(request, *args, **kwargs)


class UserDidNotAuthenticated():
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')