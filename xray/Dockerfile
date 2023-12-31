# base image to build a JRE
FROM amazoncorretto:17.0.3-alpine as corretto-jdk

# required for strip-debug to work
RUN apk add --no-cache binutils

# Build small JRE image
RUN $JAVA_HOME/bin/jlink \
         --verbose \
         --add-modules ALL-MODULE-PATH \
         --strip-debug \
         --no-man-pages \
         --no-header-files \
         --compress=2 \
         --output /customjre

# Base image
FROM python:3.9-alpine3.18

# config jre
ENV JAVA_HOME=/jre
ENV PATH="${JAVA_HOME}/bin:${PATH}"

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

# copy JRE from the base image
COPY --from=corretto-jdk /customjre $JAVA_HOME

# Expose flask webserver port
EXPOSE 8001

# Copy the Django project files
COPY . /app

# Start supervisord as the entrypoint
ENTRYPOINT ["sh", "/app/entrypoint.sh"]