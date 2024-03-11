from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
cache_dir = base_dir / 'cache'

__all__ = ['base_dir', 'cache_dir']
