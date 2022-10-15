from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, DeleteView, UpdateView, DetailView
from django.views.generic.edit import FormMixin

from board.forms import RegisterForm, BoardMessageCreateForm, CustomLoginForm, EditProfileForm, \
    CustomPasswordChangeForm, AddCommentForm
from board.models import BoardMessage, User, CommentMessage


class LoginPage(LoginView):
    """Simple login view which renders login page"""
    form_class = CustomLoginForm
    template_name = 'board/login.html'
    redirect_authenticated_user = True
    next_page = '/'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            messages.success(self.request, 'Для входа введите ваш логин и пароль.')
        return super().get_context_data(**kwargs)


class RegisterPage(FormView):
    """Users registration"""
    template_name = 'board/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_teacher')

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated:
            messages.success(self.request, 'Для регистрации заполните форму ниже')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password2'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, f'Добро пожаловать, {user}! Вы зарегистрированы!')
        if user is not None:
            login(self.request, user)
            return redirect('board')
        return super(RegisterPage, self).form_valid(form)


class BoardListView(LoginRequiredMixin, ListView):
    """Shows all the post on the main page, only for registered and authenticated users."""
    model = BoardMessage
    template_name = 'board/board.html'


class BoardMessageCreateView(LoginRequiredMixin, CreateView):
    """Creation the post for the board"""
    model = BoardMessage
    form_class = BoardMessageCreateForm
    template_name = 'board/boardmessage_create.html'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Пост {form.instance.title} добавлен')
        return super(BoardMessageCreateView, self).form_valid(form)


class BoardMessageUpdateView(LoginRequiredMixin, UpdateView):
    """Update your posts. Only you will be able to do it."""
    model = BoardMessage
    form_class = BoardMessageCreateForm
    template_name = 'board/boardmessage_update.html'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        messages.success(self.request, f'Пост {form.instance.title} обновлен')
        return super(BoardMessageUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BoardMessageUpdateView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(BoardMessageUpdateView, self).get_queryset()
        return queryset.filter(author=self.request.user).select_related('author')


class BoardMessageDeleteView(LoginRequiredMixin, DeleteView):
    """Delete your posts. Only you will be able to do it."""
    model = BoardMessage
    template_name = 'board/delete.html'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пост успешно удален!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BoardMessageDeleteView, self).get_object()
        if not obj.author == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(BoardMessageDeleteView, self).get_queryset()
        return queryset.filter(author=self.request.user).select_related('author')


class UsersListView(LoginRequiredMixin, ListView):
    """Shows all user registered on the website"""
    model = User
    template_name = 'board/users.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    """The View for the ability to change personal user's data"""
    model = User
    form_class = EditProfileForm
    template_name = 'board/edit_profile.html'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно изменен!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EditProfileView, self).get_object()
        if not obj.id == self.request.user.id:
            raise Http404
        return obj

    def get_queryset(self):
        """ Limit a User to only modifying their own data. """
        queryset = super(EditProfileView, self).get_queryset()
        return queryset.filter(id=self.request.user.id)


class CustomPasswordChangeView(PasswordChangeView):
    """Little changed PasswordChangeView because were added css classes"""
    template_name = 'board/change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш пароль изменен успешно!')
        return super().form_valid(form)


class BoardMessageDetailView(LoginRequiredMixin, DetailView, FormMixin):
    """This view shows detail about post and shows all related comments"""
    model = BoardMessage
    form_class = AddCommentForm
    template_name = 'board/board_message_detail.html'
    context_object_name = 'post'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_detail', kwargs={'pk': self.get_object().id})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('author')

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        post = self.get_object()
        self.object.board_message = post
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, 'Комментарий успешно добавлен!')
        return super().form_valid(form)


def delete_comment(request, pk):
    """
        Delete view for the comments and shows success message after
        in the same place without reloading the page. Used HTMX.
    """
    comment = get_object_or_404(CommentMessage, id=pk)
    if not comment.author == request.user:
        raise Http404
    if request.method == 'POST':
        comment.delete()
        return HttpResponse(
            '''
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                Комментарий удалён!
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>
            '''
        )
    return HttpResponseNotAllowed(["POST", ])


def edit_comment(request, pk):
    """
        Edit view for the comments and shows edited comment right after
        in the same place without reloading the page. Used HTMX.
    """
    comment = get_object_or_404(CommentMessage, id=pk)
    if not comment.author == request.user:
        raise Http404
    form = AddCommentForm(request.POST or None, instance=comment)
    post = BoardMessage.objects.get(id=comment.board_message_id)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('comment_detail', pk=comment.id)
    context = {
        'form': form,
        'comment': comment,
        'post': post
    }
    return render(request, 'board/partial/comment_form.html', context=context)


def comment_detail(request, pk):
    """Exact this view helps to the view above it. Used Htmx."""
    comment = get_object_or_404(CommentMessage, id=pk)
    if not comment.author == request.user:
        raise Http404
    context = {
        'comment': comment
    }
    return render(request, 'board/partial/comment_detail.html', context)
