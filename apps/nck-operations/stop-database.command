#!/bin/zsh
set -eu
APP_DIR="${0:A:h}"
"$APP_DIR/../../.tools/nck-runtime/bin/pg_ctl" -D "$APP_DIR/.data/postgres" stop -m fast
