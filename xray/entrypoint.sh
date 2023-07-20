#!/usr/bin/env sh

# run gunicorn with 10 workers
gunicorn webserver:app -w 10 --bind 0.0.0.0:8001