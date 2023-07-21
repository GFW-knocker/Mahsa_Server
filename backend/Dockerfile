# Base image
FROM python:3.9-alpine3.18

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install supervisord
RUN apk add supervisor

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy supervisord configuration
COPY supervisord.conf supervisord.conf

# Expose gunicron django port
EXPOSE 8000
# export supervisord interface port
EXPOSE 9001

# Copy the Django project files
COPY . .

# Start supervisord as the entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]