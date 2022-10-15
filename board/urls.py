from django.contrib.auth.views import LogoutView
from django.urls import path

from board.views import LoginPage, BoardListView, BoardMessageCreateView, BoardMessageDeleteView, RegisterPage, \
    BoardMessageUpdateView, UsersListView, EditProfileView, CustomPasswordChangeView, BoardMessageDetailView, \
    delete_comment

urlpatterns = [
    path('', BoardListView.as_view(), name='board'),
    path('login/', LoginPage.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('board_create/', BoardMessageCreateView.as_view(), name='board_create'),
    path('board_delete/<int:pk>/', BoardMessageDeleteView.as_view(), name='board_delete'),
    path('board_update/<int:pk>', BoardMessageUpdateView.as_view(), name='board_update'),
    path('users/', UsersListView.as_view(), name='users'),
    path('users/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('post_detail/<int:pk>/', BoardMessageDetailView.as_view(), name='post_detail'),
    path('comment_delete/<int:pk>/', delete_comment, name='comment_delete'),
]
