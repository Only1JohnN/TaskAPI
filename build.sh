#!/bin/bash

# === Fail fast if any command fails ===
set -e

echo "🚀 Starting deployment script..."

# === Confirm you are inside project folder ===
echo "📁 Checking project directory..."
PROJECT_DIR="$HOME/TaskAPI"
if [ "$(pwd)" != "$PROJECT_DIR" ]; then
    echo "❗ Wrong directory. Navigating to project directory..."
    cd "$PROJECT_DIR"
fi

# === Activate virtual environment ===
echo "🐍 Activating virtual environment..."
if [ ! -f "venv/bin/activate" ]; then
    echo "❗ Virtual environment not found! Exiting."
    exit 1
fi
source venv/bin/activate

# === Pull latest code from GitHub ===
echo "⬇️ Pulling latest code..."
git pull origin main

# === Install/update dependencies ===
echo "📦 Installing dependencies..."
pip install --upgrade -r requirements.txt

# === Apply database migrations ===
echo "🛠️ Applying migrations..."
python manage.py makemigrations
python manage.py migrate --noinput

# === Collect static files ===
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# === Confirm Debug setting ===
echo "⚙️ DEBUG setting:"
python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)"

# === Reload the WSGI app ===
echo "🚀 Reloading web app..."
touch /var/www/only1johnn_pythonanywhere_com_wsgi.py

echo "✅ Deployment finished successfully!"
