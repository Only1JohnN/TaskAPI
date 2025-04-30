# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . .

# Set environment variables (you might also set these in Railway)
ENV DJANGO_SETTINGS_MODULE=TaskAPI.settings
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate

# Expose the port that Gunicorn will listen on (Railway will handle the external mapping)
EXPOSE 8000

# Define the command to run the application
CMD ["gunicorn", "TaskAPI.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]