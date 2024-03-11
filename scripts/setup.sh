#!/usr/bin/env bash
set -e
basedir="$(dirname "$(dirname "$(readlink -f -- "${BASH_SOURCE[0]}")")")"
cd "$basedir/.."

VENV="$(readlink -f "$basedir/../venv")"
# torchdynamo or something doesn't support 3.12 yet
PYTHON_VERSION="3.11"
python="$(which "python$PYTHON_VERSION")"

"$python" -m venv "$VENV"
ln -sr "$basedir/sitecustomize.py" "$VENV/lib/python$PYTHON_VERSION/site-packages/sitecustomize.py"
"$VENV/bin/pip3" install -U -r "$basedir/requirements.txt"
