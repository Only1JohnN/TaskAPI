#!/bin/bash

# === Fail fast if any command fails ===
set -e

echo "🚀 Starting deployment script..."

# === Confirm you are inside project folder ===
echo "📁 Checking project directory..."
PROJECT_DIR="/app"  # This should be the directory containing 'requirements.txt' and your project files
if [ "$(pwd)" != "$PROJECT_DIR" ]; then
    echo "❗ Wrong directory. Navigating to project directory..."
    echo "Current directory: $(pwd)"

    cd "$PROJECT_DIR"
    echo "Current directory: $(pwd)"
fi

# === Search for requirements.txt file and print its location ===
echo "🔍 Searching for requirements.txt..."
REQUIREMENTS_FILE=$(find . -name "requirements.txt" -print -quit)

if [ -z "$REQUIREMENTS_FILE" ]; then
    echo "❗ requirements.txt not found! Exiting."
    exit 1
else
    echo "📄 Found requirements.txt at: $REQUIREMENTS_FILE"
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
pip install --upgrade -r "$REQUIREMENTS_FILE"  # Install the dependencies

# === Apply database migrations ===
echo "🛠️ Applying migrations..."
python3 manage.py migrate --noinput || { echo "Migrations failed"; exit 1; }

# === Collect static files ===
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

echo "✅ Deployment finished successfully!"
