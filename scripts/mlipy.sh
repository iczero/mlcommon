#!/usr/bin/env bash
basedir="$(dirname "$(dirname "$(readlink -f -- "${BASH_SOURCE[0]}")")")"
VENV="$(readlink -f "$basedir/../venv")"
exec "$VENV/bin/ipython" -i "$basedir/scripts/ipython-init.py"
