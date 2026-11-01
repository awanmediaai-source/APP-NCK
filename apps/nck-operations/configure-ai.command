#!/bin/zsh
set -eu
APP_DIR="${0:A:h}"
cd "$APP_DIR"
exec "$APP_DIR/../../.tools/nck-runtime/bin/python" configure_ai.py
