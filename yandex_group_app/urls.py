from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = f"Администрирование {settings.COMPANY}"
admin.site.site_title = f"Администрирование {settings.COMPANY}"
admin.site.index_title = f"Добро пожаловать на сервис {settings.COMPANY}"

urlpatterns = [
    path('', include('board.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
