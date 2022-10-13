from django.contrib import admin

from board.models import User, BoardMessage

admin.site.register(User)
admin.site.register(BoardMessage)

