#!/usr/bin/env sh

# run migration
./manage.py migrate

# run supervisord in non-daemon mode
supervisord -c supervisord.conf