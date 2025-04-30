#!/bin/bash

# === Fail fast if any command fails ===
set -e

echo "🚀 Starting deployment script..."

# === Confirm you are inside project folder ===
echo "📁 Checking project directory..."
PROJECT_DIR="/app/TaskAPI"  # Update this to the correct root directory on Railway
if [ "$(pwd)" != "$PROJECT_DIR" ]; then
    echo "❗ Wrong directory. Navigating to project directory..."
    echo "Current directory: $(pwd)"

    cd "$PROJECT_DIR"
fi

# === Create and activate virtual environment ===
echo "🐍 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    echo "❗ Virtual environment not found! Creating it..."
    python3 -m venv venv  # Create the virtual environment
fi
source venv/bin/activate  # Activate the virtual environment

# === Install dependencies ===
echo "📦 Installing dependencies..."
pip install --upgrade -r requirements.txt  # Install the dependencies

# === Apply database migrations ===
echo "🛠️ Applying migrations..."
python manage.py migrate --noinput

# === Collect static files ===
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# === Confirm Debug setting ===
echo "⚙️ DEBUG setting:"
python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)"

echo "✅ Deployment finished successfully!"
