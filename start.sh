#!/bin/bash

# ExitLag Free - Launch Script
echo "🚀 ExitLag Free - Configuração e Execução"
echo "========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor instale Python 3.11+"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Install requirements
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Criando arquivo .env..."
    cp .env.example .env
fi

# Run Django migrations
echo "🗃️  Executando migrações do banco..."
python manage.py makemigrations
python manage.py migrate

# Populate database with sample data
echo "📊 Populando banco com dados de exemplo..."
python manage.py populate_db

# Collect static files
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Start development server
echo "🌐 Iniciando servidor de desenvolvimento..."
echo ""
echo "✅ ExitLag Free está rodando em: http://127.0.0.1:8000"
echo "🔧 Painel Admin: http://127.0.0.1:8000/admin (admin/admin123)"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

python manage.py runserver