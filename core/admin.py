from django.contrib import admin
from .models import VPNServer, Game, UserProfile, Connection, OptimizationProfile


@admin.register(VPNServer)
class VPNServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'ping', 'load', 'is_active']
    list_filter = ['country', 'is_active']
    search_fields = ['name', 'city', 'country']
    list_editable = ['ping', 'load', 'is_active']
    ordering = ['ping', 'load']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_optimized']
    list_filter = ['category', 'is_optimized']
    search_fields = ['name', 'category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_server', 'created_at']
    list_filter = ['created_at', 'preferred_server__country']
    search_fields = ['user__username', 'user__email']


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'server', 'game', 'status', 'connected_at', 'ping_before', 'ping_after']
    list_filter = ['status', 'server__country', 'connected_at']
    search_fields = ['user__username', 'server__name', 'game__name']
    readonly_fields = ['connected_at', 'disconnected_at']


@admin.register(OptimizationProfile)
class OptimizationProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'game', 'ping_threshold', 'is_default']
    list_filter = ['game', 'is_default']
    search_fields = ['name', 'game__name']
    filter_horizontal = ['recommended_servers']