from django.contrib import admin

from board.models import User, BoardMessage, CommentMessage

admin.site.register(User)
admin.site.register(BoardMessage)
admin.site.register(CommentMessage)
