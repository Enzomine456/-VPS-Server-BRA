@echo off
REM ExitLag Free - Launch Script for Windows
echo 🚀 ExitLag Free - Configuração e Execução
echo =========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor instale Python 3.11+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate

REM Install requirements
echo 📥 Instalando dependências...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️  Criando arquivo .env...
    copy .env.example .env
)

REM Run Django migrations
echo 🗃️  Executando migrações do banco...
python manage.py makemigrations
python manage.py migrate

REM Populate database with sample data
echo 📊 Populando banco com dados de exemplo...
python manage.py populate_db

REM Collect static files
echo 📁 Coletando arquivos estáticos...
python manage.py collectstatic --noinput

REM Start development server
echo 🌐 Iniciando servidor de desenvolvimento...
echo.
echo ✅ ExitLag Free está rodando em: http://127.0.0.1:8000
echo 🔧 Painel Admin: http://127.0.0.1:8000/admin (admin/admin123)
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python manage.py runserver

pause