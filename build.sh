#!/bin/bash

# === Setup ===
echo "📁 Navigating to project directory..."
cd /home/Only1JohnN/

# === Activate virtualenv ===
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# === Pull latest code ===
echo "⬇️ Pulling latest changes from GitHub..."
git pull origin main

# === Install dependencies ===
echo "📦 Installing requirements..."
pip install -r requirements.txt

# === Apply database migrations ===
echo "🛠️ Applying migrations..."
python manage.py migrate --noinput

# === Collect static files ===
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# === Confirm Debug settings ===
echo "⚙️ DEBUG setting:"
python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)"


# === Reload the web app ===
echo "🚀 Reloading web app..."
touch /var/www/only1johnn_pythonanywhere_com_wsgi.py

echo "✅ Done! Deployed and running."
