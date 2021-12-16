#!/bin/bash
# usage: source ACTIVATE_vars_for_example.sh
export SECRET_KEY=dev
export DEBUG=True
export ALLOWED_HOSTS='127.0.0.1 localhost 0.0.0.0'
export APPEND_SLASH=True

# feedback module vars
export RECIPIENTS_EMAIL='example@gmail.com'
export DEFAULT_FROM_EMAIL='example@gmail.com'
export SENDGRID_API_KEY='SG_KEY'

# db vars
export DB_NAME='example'
export DB_USER='root'
export DB_PASSWORD='password'
export DB_HOST='db'
export DB_PORT=3306
