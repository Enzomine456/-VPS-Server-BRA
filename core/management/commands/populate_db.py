from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import VPNServer, Game, OptimizationProfile


class Command(BaseCommand):
    help = 'Populate database with sample data for ExitLag Free'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo...')

        # Create VPN Servers
        servers_data = [
            {'name': 'São Paulo Premium', 'country': 'Brasil', 'city': 'São Paulo', 
             'ip_address': '177.54.144.10', 'ping': 15, 'load': 25, 'flag_icon': '🇧🇷'},
            {'name': 'Rio de Janeiro Fast', 'country': 'Brasil', 'city': 'Rio de Janeiro', 
             'ip_address': '177.54.144.20', 'ping': 20, 'load': 30, 'flag_icon': '🇧🇷'},
            {'name': 'Brasília Connect', 'country': 'Brasil', 'city': 'Brasília', 
             'ip_address': '177.54.144.30', 'ping': 25, 'load': 35, 'flag_icon': '🇧🇷'},
            {'name': 'Buenos Aires Gaming', 'country': 'Argentina', 'city': 'Buenos Aires', 
             'ip_address': '190.12.95.10', 'ping': 45, 'load': 40, 'flag_icon': '🇦🇷'},
            {'name': 'Santiago Speed', 'country': 'Chile', 'city': 'Santiago', 
             'ip_address': '200.1.123.10', 'ping': 55, 'load': 45, 'flag_icon': '🇨🇱'},
            {'name': 'Miami East', 'country': 'Estados Unidos', 'city': 'Miami', 
             'ip_address': '208.67.222.222', 'ping': 120, 'load': 55, 'flag_icon': '🇺🇸'},
            {'name': 'Dallas Central', 'country': 'Estados Unidos', 'city': 'Dallas', 
             'ip_address': '208.67.220.220', 'ping': 135, 'load': 60, 'flag_icon': '🇺🇸'},
        ]

        for server_data in servers_data:
            server, created = VPNServer.objects.get_or_create(
                name=server_data['name'],
                defaults=server_data
            )
            if created:
                self.stdout.write(f'Servidor criado: {server.name}')

        # Create Games
        games_data = [
            {'name': 'League of Legends', 'slug': 'league-of-legends', 'category': 'MOBA',
             'description': 'MOBA competitivo da Riot Games'},
            {'name': 'Counter-Strike 2', 'slug': 'counter-strike-2', 'category': 'FPS',
             'description': 'FPS tático da Valve'},
            {'name': 'Valorant', 'slug': 'valorant', 'category': 'FPS',
             'description': 'FPS tático da Riot Games'},
            {'name': 'Free Fire', 'slug': 'free-fire', 'category': 'Battle Royale',
             'description': 'Battle Royale para dispositivos móveis'},
            {'name': 'Fortnite', 'slug': 'fortnite', 'category': 'Battle Royale',
             'description': 'Battle Royale da Epic Games'},
            {'name': 'PUBG', 'slug': 'pubg', 'category': 'Battle Royale',
             'description': 'PlayerUnknown\'s Battlegrounds'},
            {'name': 'World of Warcraft', 'slug': 'world-of-warcraft', 'category': 'MMORPG',
             'description': 'MMORPG clássico da Blizzard'},
            {'name': 'Lost Ark', 'slug': 'lost-ark', 'category': 'MMORPG',
             'description': 'MMORPG de ação da Amazon Games'},
            {'name': 'FIFA 24', 'slug': 'fifa-24', 'category': 'Sports',
             'description': 'Simulador de futebol da EA Sports'},
            {'name': 'Rocket League', 'slug': 'rocket-league', 'category': 'Sports',
             'description': 'Futebol com carros da Psyonix'},
            {'name': 'Grand Theft Auto V', 'slug': 'gta-v', 'category': 'Action',
             'description': 'Jogo de ação e aventura da Rockstar'},
            {'name': 'Apex Legends', 'slug': 'apex-legends', 'category': 'Battle Royale',
             'description': 'Battle Royale da Respawn Entertainment'},
        ]

        for game_data in games_data:
            game, created = Game.objects.get_or_create(
                slug=game_data['slug'],
                defaults=game_data
            )
            if created:
                self.stdout.write(f'Jogo criado: {game.name}')

        # Create Optimization Profiles
        profiles_data = [
            {
                'name': 'League of Legends - Brasil',
                'game': 'league-of-legends',
                'servers': ['São Paulo Premium', 'Rio de Janeiro Fast'],
                'ping_threshold': 30
            },
            {
                'name': 'CS2 - Competitivo',
                'game': 'counter-strike-2',
                'servers': ['São Paulo Premium', 'Buenos Aires Gaming'],
                'ping_threshold': 25
            },
            {
                'name': 'Valorant - Rankeada',
                'game': 'valorant',
                'servers': ['São Paulo Premium', 'Rio de Janeiro Fast'],
                'ping_threshold': 20
            },
            {
                'name': 'Free Fire - BR',
                'game': 'free-fire',
                'servers': ['São Paulo Premium', 'Rio de Janeiro Fast', 'Brasília Connect'],
                'ping_threshold': 35
            },
        ]

        for profile_data in profiles_data:
            try:
                game = Game.objects.get(slug=profile_data['game'])
                profile, created = OptimizationProfile.objects.get_or_create(
                    name=profile_data['name'],
                    game=game,
                    defaults={
                        'ping_threshold': profile_data['ping_threshold'],
                        'description': f'Perfil otimizado para {game.name}',
                        'is_default': True
                    }
                )
                
                if created:
                    # Add recommended servers
                    for server_name in profile_data['servers']:
                        try:
                            server = VPNServer.objects.get(name=server_name)
                            profile.recommended_servers.add(server)
                        except VPNServer.DoesNotExist:
                            continue
                    
                    self.stdout.write(f'Perfil criado: {profile.name}')
            except Game.DoesNotExist:
                continue

        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@exitlagfree.com',
                password='admin123',
                first_name='Admin',
                last_name='ExitLag Free'
            )
            self.stdout.write('Usuário admin criado (admin/admin123)')

        self.stdout.write(
            self.style.SUCCESS('Dados de exemplo criados com sucesso!')
        )