from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from board.models import User, BoardMessage, CommentMessage

# admin.site.register(User)
# admin.site.register(BoardMessage)
# admin.site.register(CommentMessage)


@admin.register(User)
class UserConfig(UserAdmin):
    search_fields = ('first_name', 'last_name', 'username',)
    ordering = ('-date_joined',)
    list_display = ('username', 'get_full_name', 'is_staff')
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        (_('Info'), {'fields': ('about', 'foto')}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 5, 'cols': 40})},
    }


@admin.register(CommentMessage)
class CommentMessageConfig(admin.ModelAdmin):
    search_fields = ('board_message', 'author')
    list_display = ('board_message', 'author', 'date_added', 'date_updated')
    list_filter = ("date_added", "date_updated", "author", "board_message")

    fieldsets = (
        (None, {'fields': ('board_message', 'author', 'text')}),
    )


@admin.register(BoardMessage)
class BoardMessageConfig(admin.ModelAdmin):
    search_fields = ('board_message', 'author')
    list_display = ('title', 'author', 'date_added', 'date_updated')
    list_filter = ("date_added", "date_updated", "author")

    fieldsets = (
        (None, {'fields': ('title', 'author', 'text', 'image')}),
    )
