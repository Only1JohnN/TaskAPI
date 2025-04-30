FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=TaskAPI.settings
ENV PYTHONUNBUFFERED=1
RUN SECRET_KEY=$SECRET_KEY python manage.py collectstatic --noinput
RUN SECRET_KEY=$SECRET_KEY python manage.py migrate
EXPOSE 8000
CMD ["gunicorn", "TaskAPI.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]