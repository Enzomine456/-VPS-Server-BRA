from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),
    
    # Autenticação
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Servidores
    path('servers/', views.servers, name='servers'),
    path('connect/<int:server_id>/', views.connect_server, name='connect_server'),
    path('disconnect/', views.disconnect, name='disconnect'),
    
    # Jogos
    path('games/', views.games, name='games'),
    
    # Perfil
    path('profile/', views.profile, name='profile'),
    
    # API
    path('api/status/', views.connection_status, name='connection_status'),
]