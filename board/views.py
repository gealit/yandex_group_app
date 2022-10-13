from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, CreateView, DeleteView

from board.forms import RegisterForm
from board.models import BoardMessage


class LoginPage(LoginView):
    template_name = 'board/login.html'
    redirect_authenticated_user = True
    next_page = '/'


class RegisterPage(FormView):
    template_name = 'board/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_teacher')

    def form_valid(self, form):
        user = form.save()
        user.set_password(form.cleaned_data['password2'])
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, f'Пользователь {user} зарегистрирован!')
        if user is not None:
            login(self.request, user)
            return redirect('board')
        return super(RegisterPage, self).form_valid(form)


class BoardListView(LoginRequiredMixin, ListView):
    model = BoardMessage
    template_name = 'board/board.html'


class BoardMessageCreateView(LoginRequiredMixin, CreateView):
    model = BoardMessage
    fields = ('title', 'text', 'image')
    template_name = 'board/boardmessage_create.html'
    success_url = reverse_lazy('board')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BoardMessageCreateView, self).form_valid(form)


class BoardMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = BoardMessage
    template_name = 'board/delete.html'
    success_url = reverse_lazy('board')

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
