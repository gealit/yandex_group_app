from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from board.models import User, BoardMessage, CommentMessage


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Пользователь'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Пароль'}
        )


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Имя пользователя для входа', min_length=3, max_length=30
    )
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        users = User.objects.filter(username=username)
        if users.count():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Nikname'}
        )
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Имя'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Фамилия'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Пароль'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Повторите пароль'}
        )


class BoardMessageCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BoardMessageCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = BoardMessage
        fields = ('title', 'text', 'image')


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'about')


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Введите текст комментария...'}
    ))

    class Meta:
        model = CommentMessage
        fields = ('text',)
