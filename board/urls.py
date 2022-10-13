from django.contrib.auth.views import LogoutView
from django.urls import path

from board.views import LoginPage, BoardListView, BoardMessageCreateView, BoardMessageDeleteView, RegisterPage

urlpatterns = [
    path('', BoardListView.as_view(), name='board'),
    path('board_create/', BoardMessageCreateView.as_view(), name='board_create'),
    path('board_delete/<int:pk>/', BoardMessageDeleteView.as_view(), name='board_delete'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
