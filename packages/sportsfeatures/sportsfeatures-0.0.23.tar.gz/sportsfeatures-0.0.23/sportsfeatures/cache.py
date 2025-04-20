"""Caching functionality for sportsfeatures."""

import os

from . import __VERSION__

_SPORTS_FEATURES_CACHE_FOLDER = ".sportsfeatures_" + __VERSION__


def sportsfeatures_cache_folder() -> str:
    """Return a valid cache folder."""
    if not os.path.exists(_SPORTS_FEATURES_CACHE_FOLDER):
        try:
            os.mkdir(_SPORTS_FEATURES_CACHE_FOLDER)
        except FileExistsError:
            pass
    return _SPORTS_FEATURES_CACHE_FOLDER
