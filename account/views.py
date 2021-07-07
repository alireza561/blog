from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from blog.models import Article
from category.models import Category
from comment.models import Comment
from .forms import ProfileForm
from .models import User
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, UserFieldsMixin, SuperUserAccessMixin, \
    CategoryFieldsMixin, ArticleBackAccessMixin, AdminUserAccessMixin, UserDidNotAuthenticated

# ==================================================== import register ========================================
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage


# ==================================================== import register ========================================

# @login_required
# def home(request):
#     return render(request, 'registration/home.html')


# region ArticleView
class ArticleList(LoginRequiredMixin, AdminUserAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, AdminUserAccessMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Article
    # fields = ['author', 'title', 'slug', 'category', 'description', 'thumbnail', 'publish', 'status', ]
    template_name = 'registration/article-create-update.html'


class ArticleUpdate(AdminUserAccessMixin, AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    template_name = 'registration/article-delete.html'
    success_url = reverse_lazy('account:home')


class ArticleTextForAuthor(AuthorAccessMixin, ArticleBackAccessMixin, DetailView):
    model = Article
    template_name = 'registration/article-TextForAuthor.html'


# endregion


# region UserView

class UserList(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    model = User
    template_name = 'registration/users-list.html'


class UserCreate(LoginRequiredMixin, SuperUserAccessMixin, UserFieldsMixin, FormValidMixin, CreateView):
    model = User
    template_name = 'registration/user-create-update.html'


class UserUpdate(LoginRequiredMixin, SuperUserAccessMixin, UserFieldsMixin, FormValidMixin, UpdateView):
    model = User
    template_name = 'registration/user-create-update.html'


class UserDelete(LoginRequiredMixin, SuperUserAccessMixin, DeleteView):
    model = User
    template_name = 'registration/user-delete.html'
    success_url = reverse_lazy('account:user-list')


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    # template_name = 'registration/profile.html'
    def get_template_names(self):
        if not (self.request.user.is_superuser or self.request.user.is_author or self.request.user.is_staff):
            template_name = 'registration/mini_profile.html'
        else:
            template_name = 'registration/profile.html'
        return template_name

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(UserDidNotAuthenticated, LoginView):
    def get_success_url(self):
        user = self.request.user
        if user:
            return reverse_lazy('account:profile')


# region password


class PasswordChange(PasswordChangeView):
    global usePasswordChange
    usePasswordChange = True

    def get_template_names(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_author:
            template_name = 'registration/password_change_form.html'
        else:
            template_name = 'registration/mini_password_change_form.html'
        return template_name

    success_url = reverse_lazy('password_change_done')


class PasswordChangeDone(PasswordChangeDoneView):

    def dispatch(self, request, *args, **kwargs):
        if usePasswordChange:
            return super().dispatch(request, *args, **kwargs)  # super(PasswordChangeDone, self)   is   super()
        else:
            return redirect('account:profile')

    def get_template_names(self):
        if self.request.user.is_superuser or self.request.user.is_staff or self.request.user.is_author:
            template_name = 'registration/password_change_done.html'
        else:
            template_name = 'registration/mini_password_change_done.html'
        return template_name

    usePasswordChange = False


# endregion

# endregion


# region CategoryView

class CategoryList(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    model = Category
    template_name = 'registration/category-list.html'


class CategoryCreate(LoginRequiredMixin, SuperUserAccessMixin, CategoryFieldsMixin, FormValidMixin, CreateView):
    model = Category
    template_name = 'registration/category-create-update.html'


class CategoryUpdate(LoginRequiredMixin, SuperUserAccessMixin, CategoryFieldsMixin, FormValidMixin, UpdateView):
    model = Category
    template_name = 'registration/category-create-update.html'


class CategoryDelete(LoginRequiredMixin, SuperUserAccessMixin, DeleteView):
    model = Category
    template_name = 'registration/category-delete.html'
    success_url = reverse_lazy('account:category-list')


# endregion


# region registration


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('لینک فعال سازی برای شما ارسال شد.<a href = "/login">ورود</a>')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('login')
        return HttpResponse('حساب شما با موفقیت فعال شد. برای ورود <a href = "/login">کلیک کنید</a> .')
    else:
        return HttpResponse('این لینک منقضی شده است. <a href = "/register">دوباره امتحان کنید</a> ')


# endregion

# region comments

class CommentList(LoginRequiredMixin, AdminUserAccessMixin, ListView):
    template_name = 'registration/comments_list.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()
        elif self.request.user.is_author:
            return Comment.objects.filter(user=self.request.user.is_author)

# endregion
