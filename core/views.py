from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import VPNServer, Game, Connection, OptimizationProfile, UserProfile
from .forms import CustomUserCreationForm, ProfileForm
import json


def home(request):
    """Página inicial"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'total_servers': VPNServer.objects.filter(is_active=True).count(),
        'total_games': Game.objects.filter(is_optimized=True).count(),
        'featured_games': Game.objects.filter(is_optimized=True)[:6],
    }
    return render(request, 'core/home.html', context)


def register(request):
    """Registro de usuário"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Você já pode fazer login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard principal"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Buscar conexão ativa
    active_connection = Connection.objects.filter(
        user=request.user, 
        status='connected'
    ).first()
    
    # Servidores recomendados
    recommended_servers = VPNServer.objects.filter(is_active=True).order_by('ping')[:5]
    
    # Jogos favoritos
    favorite_games = profile.favorite_games.all()[:6]
    
    # Últimas conexões
    recent_connections = Connection.objects.filter(user=request.user)[:5]
    
    context = {
        'profile': profile,
        'active_connection': active_connection,
        'recommended_servers': recommended_servers,
        'favorite_games': favorite_games,
        'recent_connections': recent_connections,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def servers(request):
    """Lista de servidores VPN"""
    country = request.GET.get('country')
    search = request.GET.get('search')
    
    servers = VPNServer.objects.filter(is_active=True)
    
    if country:
        servers = servers.filter(country=country)
    
    if search:
        servers = servers.filter(
            Q(name__icontains=search) | 
            Q(city__icontains=search) | 
            Q(country__icontains=search)
        )
    
    servers = servers.order_by('ping', 'load')
    
    # Países disponíveis
    countries = VPNServer.objects.filter(is_active=True).values_list('country', flat=True).distinct()
    
    context = {
        'servers': servers,
        'countries': countries,
        'selected_country': country,
        'search_query': search,
    }
    return render(request, 'core/servers.html', context)


@login_required
def games(request):
    """Lista de jogos suportados"""
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    games = Game.objects.filter(is_optimized=True)
    
    if category:
        games = games.filter(category=category)
    
    if search:
        games = games.filter(Q(name__icontains=search))
    
    games = games.order_by('name')
    
    # Categorias disponíveis
    categories = Game.objects.filter(is_optimized=True).values_list('category', flat=True).distinct()
    
    context = {
        'games': games,
        'categories': categories,
        'selected_category': category,
        'search_query': search,
    }
    return render(request, 'core/games.html', context)


@login_required
def connect_server(request, server_id):
    """Conectar a um servidor VPN"""
    if request.method == 'POST':
        server = get_object_or_404(VPNServer, id=server_id, is_active=True)
        
        # Desconectar conexões ativas
        Connection.objects.filter(user=request.user, status='connected').update(status='disconnected')
        
        # Criar nova conexão
        connection = Connection.objects.create(
            user=request.user,
            server=server,
            status='connecting',
            ping_before=request.POST.get('ping_before', 0)
        )
        
        # Simular conexão (em produção, aqui seria a lógica real de VPN)
        connection.status = 'connected'
        connection.ping_after = max(10, server.ping - 20)  # Simular melhoria no ping
        connection.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Conectado ao servidor {server.name}',
            'server_name': server.name,
            'ping_improvement': connection.ping_before - connection.ping_after
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def disconnect(request):
    """Desconectar do servidor VPN"""
    if request.method == 'POST':
        active_connections = Connection.objects.filter(user=request.user, status='connected')
        
        for connection in active_connections:
            connection.status = 'disconnected'
            connection.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Desconectado com sucesso'
        })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})


@login_required
def profile(request):
    """Perfil do usuário"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)


@login_required
def connection_status(request):
    """API para status da conexão"""
    active_connection = Connection.objects.filter(
        user=request.user, 
        status='connected'
    ).first()
    
    if active_connection:
        return JsonResponse({
            'connected': True,
            'server_name': active_connection.server.name,
            'server_country': active_connection.server.country,
            'server_city': active_connection.server.city,
            'ping': active_connection.ping_after,
            'connected_since': active_connection.connected_at.isoformat() if active_connection.connected_at else None,
        })
    else:
        return JsonResponse({'connected': False})