from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from core.models import VPNServer, Game, Connection, UserProfile
from .serializers import VPNServerSerializer, GameSerializer, ConnectionSerializer, UserProfileSerializer


class VPNServerViewSet(viewsets.ReadOnlyModelViewSet):
    """API para servidores VPN"""
    queryset = VPNServer.objects.filter(is_active=True)
    serializer_class = VPNServerSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_country(self, request):
        """Agrupa servidores por país"""
        servers = self.get_queryset()
        countries = {}
        
        for server in servers:
            if server.country not in countries:
                countries[server.country] = []
            countries[server.country].append(VPNServerSerializer(server).data)
        
        return Response(countries)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Servidores recomendados baseado no ping"""
        servers = self.get_queryset().order_by('ping', 'load')[:5]
        serializer = self.get_serializer(servers, many=True)
        return Response(serializer.data)


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """API para jogos"""
    queryset = Game.objects.filter(is_optimized=True)
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Agrupa jogos por categoria"""
        games = self.get_queryset()
        categories = {}
        
        for game in games:
            if game.category not in categories:
                categories[game.category] = []
            categories[game.category].append(GameSerializer(game).data)
        
        return Response(categories)


class ConnectionViewSet(viewsets.ReadOnlyModelViewSet):
    """API para conexões do usuário"""
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Connection.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Conexão ativa do usuário"""
        connection = self.get_queryset().filter(status='connected').first()
        if connection:
            serializer = self.get_serializer(connection)
            return Response(serializer.data)
        return Response({'message': 'Nenhuma conexão ativa'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def connect(self, request):
        """Conectar a um servidor"""
        server_id = request.data.get('server_id')
        game_id = request.data.get('game_id')
        
        if not server_id:
            return Response({'error': 'ID do servidor é obrigatório'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        server = get_object_or_404(VPNServer, id=server_id, is_active=True)
        game = None
        if game_id:
            game = get_object_or_404(Game, id=game_id)
        
        # Desconectar conexões ativas
        self.get_queryset().filter(status='connected').update(status='disconnected')
        
        # Criar nova conexão
        connection = Connection.objects.create(
            user=request.user,
            server=server,
            game=game,
            status='connected',
            ping_before=request.data.get('ping_before', 0),
            ping_after=max(10, server.ping - 20)
        )
        
        serializer = self.get_serializer(connection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def disconnect(self, request):
        """Desconectar do servidor"""
        connections = self.get_queryset().filter(status='connected')
        connections.update(status='disconnected')
        
        return Response({'message': 'Desconectado com sucesso'})


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """API para perfil do usuário"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return UserProfile.objects.filter(user=self.request.user)