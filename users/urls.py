from django.urls import path
from django.contrib.auth.views import LoginView
from .views import UserCreateView, logout_view, confirm_email, UserListView, UserDetailView, UserUpdateView

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-confirm/<str:token>/', confirm_email, name='email-confirm'),

    path('users_list/', UserListView.as_view(), name='users_list'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update')
]
