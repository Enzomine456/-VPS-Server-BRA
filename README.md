# VPS Server BRA - Gaming VPN Optimization Platform

A Django-based web application that provides VPN server optimization for gaming, offering reduced latency and improved connection quality for online games.

## 🎮 Features

- **VPN Server Management**: Multiple server locations across different countries
- **Game Optimization**: Specialized optimization profiles for popular games
- **Real-time Monitoring**: Ping monitoring and server load tracking
- **User Profiles**: Personalized settings and favorite games
- **Connection History**: Track your connection sessions and performance
- **REST API**: Full API support for mobile/desktop clients

## 🚀 Technologies

- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Fly.io ready with Docker support
- **Authentication**: Django built-in authentication system

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- See `requirements.txt` for full dependency list

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Enzomine456/VPS-Server-BRA.git
   cd VPS-Server-BRA
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOST=localhost
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Populate initial data (optional)**
   ```bash
   python manage.py populate_db
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🌐 Usage

1. **Access the application**: Open http://localhost:8000
2. **Register/Login**: Create an account or login with existing credentials
3. **Browse Servers**: View available VPN servers and their status
4. **Select Games**: Choose your favorite games for optimization
5. **Connect**: Establish VPN connections with optimized settings

## 📱 API Endpoints

The application provides a REST API with the following main endpoints:

- `/api/servers/` - VPN servers management
- `/api/games/` - Games catalog
- `/api/connections/` - Connection management
- `/api/profiles/` - User profiles

## 🐳 Docker Deployment

The project includes Docker configuration for easy deployment:

```bash
docker build -t vps-server-bra .
docker run -p 8000:8000 vps-server-bra
```

## ☁️ Fly.io Deployment

The project is configured for Fly.io deployment:

```bash
fly deploy
```

## 🗂️ Project Structure

```
VPS-Server-BRA/
├── api/                 # REST API application
├── core/                # Main application logic
├── exitlag_free/        # Django project settings
├── static/              # Static files (CSS, JS)
├── templates/           # HTML templates
├── requirements.txt     # Python dependencies
├── manage.py           # Django management script
├── Dockerfile          # Docker configuration
└── fly.toml            # Fly.io deployment config
```

## 🎯 Models

- **VPNServer**: Server information and status
- **Game**: Supported games catalog
- **UserProfile**: User preferences and settings
- **Connection**: VPN connection sessions
- **OptimizationProfile**: Game-specific optimization settings

## 🔧 Configuration

### Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOST`: Allowed hosts for production
- `DATABASE_URL`: Database connection string (production)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions, please create an issue on GitHub.

## 🎮 Gaming Performance

This platform is designed to optimize gaming connections by:
- Selecting optimal server routes
- Reducing packet loss
- Minimizing latency
- Providing stable connections

---

**Made with ❤️ for gamers who demand the best connection quality**