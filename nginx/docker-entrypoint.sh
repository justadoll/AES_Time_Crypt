#!/bin/sh
set -e

envsubst '${DOMAIN}' < /etc/nginx/nginx.conf > /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'