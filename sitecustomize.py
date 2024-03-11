import os

# TODO: is it a good idea to hijack sitecustomize?

if os.environ.get('MLCOMMON_DISABLE') != '1':
    import sys
    from pathlib import Path

    basedir = Path(__file__).resolve().parent
    sys.path.insert(0, str(basedir / 'modules'))

    from mlcommon import site_init
    site_init()
