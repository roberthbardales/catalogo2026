from django.urls import path

from . import views

app_name = 'app_users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('update/', views.UpdatePasswordView.as_view(), name='user-update'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/edit/', views.UserUpdateView.as_view(), name='user-edit'),
    path('users/<int:user_id>/toggle-active/', views.ToggleUserActiveView.as_view(), name='user-toggle-active'),
    path('users/<int:user_id>/reset-password/', views.AdminResetPasswordView.as_view(), name='user-reset-password'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('', views.PerfilView.as_view(), name='perfil'),
]
