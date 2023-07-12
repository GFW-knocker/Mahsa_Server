# Base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy supervisord configuration
COPY supervisord.conf supervisord.conf

# Copy the Django project files
COPY . .

# Expose gunicron django port
EXPOSE 8000
# export supervisord interface port
EXPOSE 9001

# Start supervisord as the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]