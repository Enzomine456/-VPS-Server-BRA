from rest_framework import serializers
from core.models import VPNServer, Game, Connection, UserProfile


class VPNServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VPNServer
        fields = ['id', 'name', 'country', 'city', 'ping', 'load', 'flag_icon']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'slug', 'icon', 'category', 'description']


class ConnectionSerializer(serializers.ModelSerializer):
    server = VPNServerSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    
    class Meta:
        model = Connection
        fields = ['id', 'server', 'game', 'status', 'connected_at', 
                 'ping_before', 'ping_after', 'duration']


class UserProfileSerializer(serializers.ModelSerializer):
    preferred_server = VPNServerSerializer(read_only=True)
    favorite_games = GameSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['preferred_server', 'favorite_games', 'created_at']