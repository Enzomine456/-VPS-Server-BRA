from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class VPNServer(models.Model):
    """Modelo para servidores VPN"""
    name = models.CharField(max_length=100, verbose_name="Nome")
    country = models.CharField(max_length=50, verbose_name="País")
    city = models.CharField(max_length=50, verbose_name="Cidade")
    ip_address = models.GenericIPAddressField(verbose_name="Endereço IP")
    ping = models.IntegerField(default=0, verbose_name="Ping (ms)")
    load = models.IntegerField(default=0, verbose_name="Carga (%)")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    flag_icon = models.CharField(max_length=10, verbose_name="Ícone da Bandeira")
    
    class Meta:
        verbose_name = "Servidor VPN"
        verbose_name_plural = "Servidores VPN"
        ordering = ['ping', 'load']
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"


class Game(models.Model):
    """Modelo para jogos suportados"""
    name = models.CharField(max_length=100, verbose_name="Nome")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    icon = models.ImageField(upload_to='games/', blank=True, null=True, verbose_name="Ícone")
    category = models.CharField(max_length=50, verbose_name="Categoria")
    is_optimized = models.BooleanField(default=True, verbose_name="Otimizado")
    description = models.TextField(blank=True, verbose_name="Descrição")
    
    class Meta:
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Perfil do usuário"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    preferred_server = models.ForeignKey(VPNServer, on_delete=models.SET_NULL, 
                                       null=True, blank=True, verbose_name="Servidor Preferido")
    favorite_games = models.ManyToManyField(Game, blank=True, verbose_name="Jogos Favoritos")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis dos Usuários"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class Connection(models.Model):
    """Modelo para conexões VPN"""
    STATUS_CHOICES = [
        ('disconnected', 'Desconectado'),
        ('connecting', 'Conectando'),
        ('connected', 'Conectado'),
        ('disconnecting', 'Desconectando'),
        ('error', 'Erro'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    server = models.ForeignKey(VPNServer, on_delete=models.CASCADE, verbose_name="Servidor")
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Jogo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                            default='disconnected', verbose_name="Status")
    connected_at = models.DateTimeField(null=True, blank=True, verbose_name="Conectado em")
    disconnected_at = models.DateTimeField(null=True, blank=True, verbose_name="Desconectado em")
    ping_before = models.IntegerField(default=0, verbose_name="Ping Antes (ms)")
    ping_after = models.IntegerField(default=0, verbose_name="Ping Depois (ms)")
    
    class Meta:
        verbose_name = "Conexão"
        verbose_name_plural = "Conexões"
        ordering = ['-connected_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.server.name} ({self.status})"
    
    @property
    def duration(self):
        if self.connected_at and self.disconnected_at:
            return self.disconnected_at - self.connected_at
        elif self.connected_at:
            return timezone.now() - self.connected_at
        return None


class OptimizationProfile(models.Model):
    """Perfis de otimização para jogos"""
    name = models.CharField(max_length=100, verbose_name="Nome")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name="Jogo")
    recommended_servers = models.ManyToManyField(VPNServer, verbose_name="Servidores Recomendados")
    ping_threshold = models.IntegerField(default=50, verbose_name="Limite de Ping (ms)")
    description = models.TextField(blank=True, verbose_name="Descrição")
    is_default = models.BooleanField(default=False, verbose_name="Perfil Padrão")
    
    class Meta:
        verbose_name = "Perfil de Otimização"
        verbose_name_plural = "Perfis de Otimização"
    
    def __str__(self):
        return f"{self.name} - {self.game.name}"