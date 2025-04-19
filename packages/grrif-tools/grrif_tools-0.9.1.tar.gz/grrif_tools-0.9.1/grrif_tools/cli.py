"""
Command-line interface for GRRIF Tools.
"""
import sys
import argparse
from datetime import date, datetime
from typing import Optional, List, Dict, Any

from .version import __version__
from .utils import Config, logger
from .grrif_archiver import plays_to_db, plays_to_txt, plays_to_stdout
from .grrif_player import start_playback, stop_playback
from .grrif_scrobbler import start_scrobbling, authenticate_lastfm
from .grrif_stats import get_top_artists, get_top_tracks
from .tui import run_tui

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=f"GRRIF Tools v{__version__}: A set of tools for Cool Cats™. "
                    f"Allows you to archive GRRIF's play history, view stats, "
                    f"stream the radio, and scrobble to Last.fm."
    )
    
    # Global arguments
    parser.add_argument(
        "--tui", 
        action="store_true", 
        help="Launch the terminal user interface"
    )
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest="command")
    
    # Archive command
    archive_parser = subparsers.add_parser(
        "archive", 
        help="Archive GRRIF's play history."
    )
    archive_parser.add_argument(
        "destination",
        choices=["print", "db", "txt"],
        help="Specify where to archive the play history (print to stdout, save to SQLite database, or to text files)."
    )
    archive_parser.add_argument(
        "from_date",
        nargs="?",
        default="2021-01-01",
        help="Specify the start date for the archive in YYYY-MM-DD format. Defaults to 2021-01-01."
    )
    archive_parser.add_argument(
        "to_date",
        nargs="?",
        default=date.today().strftime("%Y-%m-%d"),
        help=f"Specify the end date for the archive in YYYY-MM-DD format. Defaults to today ({date.today().strftime('%Y-%m-%d')})."
    )
    
    # Stats command
    stats_parser = subparsers.add_parser(
        "stats", 
        help="Get statistics from the play history."
    )
    stats_subparsers = stats_parser.add_subparsers(dest="stats_command")
    
    # Artists stats
    artists_parser = stats_subparsers.add_parser(
        "artists", 
        help="Display statistics for artists"
    )
    artists_parser.add_argument(
        "topofthepop",
        choices=["top10", "top25", "top100"],
        help="Display the top 10, 25 or 100 artists."
    )
    artists_parser.add_argument(
        "from_date",
        nargs="?",
        default="2021-01-01",
        help="Specify the start date for the stats in YYYY-MM-DD format. Defaults to 2021-01-01."
    )
    artists_parser.add_argument(
        "to_date",
        nargs="?",
        default=date.today().strftime("%Y-%m-%d"),
        help=f"Specify the end date for the stats in YYYY-MM-DD format. Defaults to today ({date.today().strftime('%Y-%m-%d')})."
    )
    
    # Tracks stats
    tracks_parser = stats_subparsers.add_parser(
        "tracks", 
        help="Display statistics for tracks"
    )
    tracks_parser.add_argument(
        "topofthepop",
        choices=["top10", "top25", "top100"],
        help="Display the top 10, 25 or 100 tracks."
    )
    tracks_parser.add_argument(
        "from_date",
        nargs="?",
        default="2021-01-01",
        help="Specify the start date for the stats in YYYY-MM-DD format. Defaults to 2021-01-01."
    )
    tracks_parser.add_argument(
        "to_date",
        nargs="?",
        default=date.today().strftime("%Y-%m-%d"),
        help=f"Specify the end date for the stats in YYYY-MM-DD format. Defaults to today ({date.today().strftime('%Y-%m-%d')})."
    )
    
    # Scrobble command
    scrobble_parser = subparsers.add_parser(
        "scrobble",
        help="Scrobble to Last.fm."
    )
    scrobble_subparsers = scrobble_parser.add_subparsers(dest="scrobble_command")
    
    # Scrobble settings
    settings_parser = scrobble_subparsers.add_parser(
        "settings", 
        help="Set your Last.fm scrobbling settings"
    )
    settings_parser.add_argument(
        "api_key",
        help="Your Last.fm API Key"
    )
    settings_parser.add_argument(
        "api_secret",
        help="Your Last.fm API Secret"
    )
    settings_parser.add_argument(
        "session_key",
        help="Your Last.fm API Session Key"
    )
    
    # Start scrobbling
    scrobble_subparsers.add_parser(
        "start", 
        help="Start scrobbling to Last.fm now."
    )
    
    # Play command
    play_parser = subparsers.add_parser(
        "play",
        help="Stream GRRIF radio in the console."
    )
    play_parser.add_argument(
        "quality",
        choices=["mp3_high", "mp3_low", "aac_high"],
        nargs="?",
        default="mp3_high",
        help="Specify streaming quality (default: mp3_high)"
    )

    # Add authenticate command
    auth_parser = scrobble_subparsers.add_parser(
        "authenticate", 
        help="Authenticate with Last.fm and obtain a session key"
    )
    auth_parser.add_argument(
        "api_key",
        help="Your Last.fm API Key"
    )
    auth_parser.add_argument(
        "api_secret",
        help="Your Last.fm API Secret"
    )
    
    return parser.parse_args()

def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()
    
    print(
        "##########################################\n"
        f"##### [ GRRIF Tools version {__version__} ] ######\n"
        "##########################################\n"
    )
    
    # Launch TUI if requested
    if args.tui:
        run_tui()
        return
    
    # If no command is given, show help
    if not args.command and len(sys.argv) == 1:
        print("No command specified. Use --help for usage information.")
        sys.exit(1)
    
    # Handle archive command
    if args.command == "archive":
        # Set the base URL to scrape data from
        base_url = "https://www.grrif.ch/recherche-de-titres/?date={}"
        
        # Set the date range
        start_date = datetime.strptime(args.from_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.to_date, "%Y-%m-%d")
        
        # Archive to database
        if args.destination == "db":
            print(f"Archiving plays from {args.from_date} to {args.to_date} to database...")
            plays_to_db(base_url, start_date, end_date)
        
        # Archive to text files
        elif args.destination == "txt":
            print(f"Archiving plays from {args.from_date} to {args.to_date} to text files...")
            plays_to_txt(base_url, start_date, end_date)
        
        # Print to stdout
        elif args.destination == "print":
            print(f"Displaying plays from {args.from_date} to {args.to_date}:")
            plays_to_stdout(base_url, start_date, end_date)
    
    # Handle stats command
    elif args.command == "stats":
        if not args.stats_command:
            print("Please specify a stats command (artists or tracks).")
            sys.exit(1)
        
        # Set the date range
        start_date = datetime.strptime(args.from_date, "%Y-%m-%d")
        end_date = datetime.strptime(args.to_date, "%Y-%m-%d")
        
        # Get limit from topofthepop argument
        limit = int(args.topofthepop.replace("top", ""))
        
        # Get artist stats
        if args.stats_command == "artists":
            print(f"Top {limit} artists from {args.from_date} to {args.to_date}:")
            artists = get_top_artists(limit, start_date, end_date)
            
            for i, (artist, plays) in enumerate(artists, 1):
                print(f"{i}. {artist} ({plays} plays)")
        
        # Get track stats
        elif args.stats_command == "tracks":
            print(f"Top {limit} tracks from {args.from_date} to {args.to_date}:")
            tracks = get_top_tracks(limit, start_date, end_date)
            
            for i, (artist, title, plays) in enumerate(tracks, 1):
                print(f"{i}. {artist} - {title} ({plays} plays)")
    
    # Handle scrobble command
    elif args.command == "scrobble":
        if not args.scrobble_command:
            print("Please specify a scrobble command (settings or start).")
            sys.exit(1)
        
        # Set Last.fm credentials
        if args.scrobble_command == "settings":
            config = Config()
            config.set_lastfm_credentials(
                args.api_key,
                args.api_secret,
                args.session_key
            )
            print("Last.fm credentials saved successfully.")
            
        # Authenticate with Last.fm
        elif args.scrobble_command == "authenticate":
            print("Starting Last.fm authentication process...")
            result = authenticate_lastfm(args.api_key, args.api_secret)
            
            if 'success' in result and result['success']:
                config = Config()
                config.set_lastfm_credentials(
                    args.api_key,
                    args.api_secret,
                    result['session_key']
                )
                print(f"\nAuthentication successful!")
                print(f"Username: {result['username']}")
                print(f"Session key: {result['session_key']}")
                print("\nCredentials have been saved. You can now use 'grrif_tools scrobble start' to begin scrobbling.")
            else:
                error_code = result.get('error', 'unknown')
                error_message = result.get('message', 'Unknown error')
                print(f"\nAuthentication failed: {error_code} - {error_message}")
        
        # Start scrobbling
        elif args.scrobble_command == "start":
            start_scrobbling()
    
    # Handle play command
    elif args.command == "play":
        start_playback(args.quality)