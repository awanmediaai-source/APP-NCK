#!/bin/zsh
set -eu
APP_DIR="${0:A:h}"
RUNTIME_DIR="$APP_DIR/../../.tools/nck-runtime"
export PATH="$RUNTIME_DIR/bin:$PATH"
cd "$APP_DIR"
mkdir -p .data
if [[ ! -f .secret ]]; then python -c 'import secrets,pathlib; pathlib.Path(".secret").write_text(secrets.token_urlsafe(64))'; chmod 600 .secret; fi
if [[ ! -f .data/postgres/PG_VERSION ]]; then
  initdb -D "$APP_DIR/.data/postgres" --encoding=UTF8 --locale=C --auth-local=trust --auth-host=trust > .data/init.log
  cat >> .data/postgres/postgresql.conf <<'CONFIG'
listen_addresses = '127.0.0.1'
port = 55432
unix_socket_directories = '/private/tmp'
CONFIG
fi
if ! pg_ctl -D "$APP_DIR/.data/postgres" status >/dev/null 2>&1; then
  pg_ctl -D "$APP_DIR/.data/postgres" -l "$APP_DIR/.data/postgres.log" start
fi
if ! psql -h 127.0.0.1 -p 55432 -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='nck_operations'" | /usr/bin/grep -q 1; then
  createdb -h 127.0.0.1 -p 55432 nck_operations
fi
python manage.py migrate --noinput
python manage.py seed_demo
printf '\nNCK siap di http://127.0.0.1:8000 — Ctrl+C untuk menghentikan web.\n'
exec python manage.py runserver 127.0.0.1:8000 --noreload
