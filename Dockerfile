# Stage 1: Collect static files from Django
FROM python:3.8 AS django-static

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY backend .

# Collect static files
RUN python manage.py collectstatic --noinput

# Stage 2: Build Vue.js app and copy dist files to Nginx
FROM node:18 AS vue-build

WORKDIR /app

# Copy Vue.js project files
COPY frontend/package.json frontend/package.json ./
COPY frontend/package-lock.json frontend/package-lock.json ./

# Install dependencies
RUN npm ci

COPY frontend .

# Build Vue.js app
RUN npm run build


# Stage 3: Create final Nginx image and copy static files
FROM nginx:1.21

# Copy static files from Django
COPY --from=django-static /app/staticfiles/ /var/www/static/

# Copy built dist files from Vue.js
COPY --from=vue-build /app/dist/ /var/www/html/

# Copy Nginx configuration
COPY nginx/default.conf /etc/nginx/conf.d/default.conf