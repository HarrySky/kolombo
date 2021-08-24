#!/bin/bash
set -e

find kolombo -type d -name __pycache__ -exec rm -r {} \+

# Trust nginx with real IP addresses
export FORWARDED_ALLOW_IPS=192.168.79.120
exec uvicorn kolombo.auth.api:app --host=0.0.0.0 --port 7089 \
    --loop=uvloop --http httptools --interface asgi3 \
    --proxy-headers --use-colors
