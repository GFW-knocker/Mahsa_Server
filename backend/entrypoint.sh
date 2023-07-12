#!/usr/bin/env bash

# run migration
./manage.py migrate

# run supervisord in non-daemon mode
supervisord -c supervisord.conf