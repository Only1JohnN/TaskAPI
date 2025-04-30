FROM python:3.12-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=TaskAPI.settings
ENV PYTHONUNBUFFERED=1
# Explicitly set the SECRET_KEY environment variable
ENV SECRET_KEY=$SECRET_KEY
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate
EXPOSE 8000
CMD ["gunicorn", "TaskAPI.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]