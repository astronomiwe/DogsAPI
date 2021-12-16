#!/bin/bash
# убираем переменные из venv

# django vars
unset SECRET_KEY
unset DEBUG
unset ALLOWED_HOSTS
unset APPEND_SLASH

# feedback module vars
unset RECIPIENTS_EMAIL
unset DEFAULT_FROM_EMAIL
unset SENDGRID_API_KEY

# db vars
unset DB_NAME
unset DB_USER
unset DB_PASSWORD
unset DB_HOST
unset DB_PORT