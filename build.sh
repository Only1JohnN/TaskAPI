python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Explicitly set SECRET_KEY for the collectstatic command
export SECRET_KEY="$SECRET_KEY"
python manage.py collectstatic --noinput

python manage.py migrate