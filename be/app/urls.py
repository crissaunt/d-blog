from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    CurrentUserView,
    CategoryListCreateView,
    BlogPostListCreateView,
    BlogPostDetailView,
    AdminStatsView,
    AdminUserListView,
    AdminUserDetailView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/me/', CurrentUserView.as_view(), name='auth_me'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('categories/', CategoryListCreateView.as_view(), name='category_list_create'),

    # Blog 
    path('blogs/', BlogPostListCreateView.as_view(), name='blog_list_create'),
    path('blogs/<slug:slug>/', BlogPostDetailView.as_view(), name='blog_detail'),

    # Admin 
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('admin/users/', AdminUserListView.as_view(), name='admin_users'),
    path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin_user_detail'),
]
