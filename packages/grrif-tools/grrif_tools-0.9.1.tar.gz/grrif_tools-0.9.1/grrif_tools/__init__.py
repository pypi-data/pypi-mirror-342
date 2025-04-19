"""
GRRIF Tools - A set of tools for Cool Cats™.

This package provides tools to archive GRRIF's play history,
compute stats, stream the radio, and scrobble to last.fm.
"""
from .version import __version__

# Import main components for easier access
from .grrif_archiver import plays_to_db, plays_to_txt, plays_to_stdout
from .grrif_stats import get_top_artists, get_top_tracks
from .grrif_player import start_playback, stop_playback
from .grrif_scrobbler import start_scrobbling, authenticate_lastfm

__all__ = [
    "__version__",
    "plays_to_db",
    "plays_to_txt", 
    "plays_to_stdout",
    "get_top_artists",
    "get_top_tracks",
    "start_playback",
    "stop_playback",
    "start_scrobbling",
    "authenticate_lastfm"
]