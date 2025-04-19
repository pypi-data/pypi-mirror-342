"""
Terminal User Interface for GRRIF Tools.

This module provides a user-friendly TUI using the Textual library.
"""
import asyncio
from datetime import date, datetime, timedelta
import threading
import time
from typing import Optional, List, Dict, Any, Callable

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, Select, Label
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.binding import Binding

from .version import __version__
from .utils import Config, logger
from .grrif_archiver import plays_to_db, plays_to_txt, plays_to_stdout
from .grrif_stats import get_top_artists, get_top_tracks
from .grrif_player import start_playback, stop_playback
from .grrif_scrobbler import TrackScrobbler

# Base URL for GRRIF play history
BASE_URL = "https://www.grrif.ch/recherche-de-titres/?date={}"

class TaskScreen(Screen):
    """Base screen for long-running tasks."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_flag = threading.Event()
        self._task_thread = None
        
    def start_task(self, task_func: Callable, *args, **kwargs):
        """Start a task in a separate thread."""
        self._stop_flag.clear()
        self._task_thread = threading.Thread(
            target=task_func,
            args=args,
            kwargs=kwargs,
            daemon=True
        )
        self._task_thread.start()
        
    def stop_task(self):
        """Stop the running task."""
        if self._task_thread and self._task_thread.is_alive():
            self._stop_flag.set()
            self._task_thread.join(timeout=1)
            
    def on_unmount(self):
        """Clean up when screen is unmounted."""
        self.stop_task()

class GRRIFApp(App):
    """Main GRRIF Tools TUI application."""
    
    CSS_PATH = "grrif.css"
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("b", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header(f"GRRIF Tools v{__version__}")
        
        with Container(id="main"):
            with Horizontal(id="buttons"):
                yield Button("Archive", id="btn-archive", variant="primary")
                yield Button("Stats", id="btn-stats", variant="primary")
                yield Button("Stream", id="btn-stream", variant="primary")
                yield Button("Scrobble", id="btn-scrobble", variant="primary")
                yield Button("Settings", id="btn-settings", variant="primary")
            
            # Default welcome screen
            yield Static(f"Welcome to GRRIF Tools v{__version__}\n\nA set of tools for Cool Cats™", id="welcome")
            
        yield Footer()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "btn-archive":
            self.push_screen(ArchiveScreen())
        elif button_id == "btn-stats":
            self.push_screen(StatsScreen())
        elif button_id == "btn-stream":
            self.push_screen(StreamScreen())
        elif button_id == "btn-scrobble":
            self.push_screen(ScrobbleScreen())
        elif button_id == "btn-settings":
            self.push_screen(SettingsScreen())
    
    def action_go_back(self):
        """Handle the 'back' action."""
        self.pop_screen()
    
    def action_quit(self):
        """Handle the 'quit' action."""
        self.exit()

class ArchiveScreen(Screen):
    """Screen for archiving GRRIF play history."""
    
    BINDINGS = [
        Binding("b", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for archive screen."""
        yield Header()
        
        with Container():
            yield Static("Archive GRRIF's Play History", id="screen-title")
            
            with Vertical():
                yield Static("Select destination:")
                with Horizontal():
                    yield Button("Database", id="dest-db", variant="primary")
                    yield Button("Text Files", id="dest-txt", variant="primary")
                    yield Button("Print", id="dest-print", variant="primary")
                
                yield Static("Date Range:")
                with Horizontal():
                    yield Static("From:", classes="label")
                    yield Input(placeholder="YYYY-MM-DD", id="from-date", value="2021-01-01")
                    yield Static("To:", classes="label")
                    yield Input(placeholder="YYYY-MM-DD", id="to-date", value=date.today().strftime("%Y-%m-%d"))
                
                yield Button("Start Archiving", id="start-archive")
                
                yield Static("", id="archive-status")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses on archive screen."""
        button_id = event.button.id
        
        if button_id == "dest-db":
            self.selected_dest = "db"
            self.update_status("Selected destination: Database")
        elif button_id == "dest-txt":
            self.selected_dest = "txt"
            self.update_status("Selected destination: Text Files")
        elif button_id == "dest-print":
            self.selected_dest = "print"
            self.update_status("Selected destination: Print to Console")
        elif button_id == "start-archive":
            self.start_archiving()
    
    def on_mount(self):
        """Initialize screen state when mounted."""
        self.selected_dest = None
    
    def update_status(self, message: str):
        """Update the status display."""
        self.query_one("#archive-status").update(message)
    
    def start_archiving(self):
        """Start the archiving process."""
        if not self.selected_dest:
            self.update_status("Please select a destination first.")
            return
        
        try:
            from_date = datetime.strptime(self.query_one("#from-date").value, "%Y-%m-%d")
            to_date = datetime.strptime(self.query_one("#to-date").value, "%Y-%m-%d")
            
            if from_date > to_date:
                self.update_status("Error: From date must be before To date.")
                return
            
            self.update_status(f"Archiving from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}...")
            
            # Start archiving in a background thread
            def archive_task():
                try:
                    if self.selected_dest == "db":
                        plays_to_db(BASE_URL, from_date, to_date)
                    elif self.selected_dest == "txt":
                        plays_to_txt(BASE_URL, from_date, to_date)
                    elif self.selected_dest == "print":
                        plays_to_stdout(BASE_URL, from_date, to_date)
                    
                    # Update status when complete
                    self.app.call_from_thread(
                        self.update_status,
                        f"Archiving completed successfully to {self.selected_dest}."
                    )
                except Exception as e:
                    # Update status with error
                    self.app.call_from_thread(
                        self.update_status,
                        f"Error during archiving: {str(e)}"
                    )
            
            threading.Thread(target=archive_task, daemon=True).start()
            
        except ValueError:
            self.update_status("Error: Invalid date format. Use YYYY-MM-DD.")
    
    def action_go_back(self):
        """Handle the 'back' action."""
        self.app.pop_screen()

class StatsScreen(Screen):
    """Screen for viewing GRRIF stats."""
    
    BINDINGS = [
        Binding("b", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for stats screen."""
        yield Header()
        
        with Container():
            yield Static("View Statistics", id="screen-title")
            
            with Vertical():
                yield Static("Select type:")
                with Horizontal():
                    yield Button("Artists", id="type-artists", variant="primary")
                    yield Button("Tracks", id="type-tracks", variant="primary")
                
                yield Static("Select count:")
                with Horizontal():
                    yield Button("Top 10", id="count-10", variant="primary")
                    yield Button("Top 25", id="count-25", variant="primary")
                    yield Button("Top 100", id="count-100", variant="primary")
                
                yield Static("Date Range:")
                with Horizontal():
                    yield Static("From:", classes="label")
                    yield Input(placeholder="YYYY-MM-DD", id="from-date", value="2021-01-01")
                    yield Static("To:", classes="label")
                    yield Input(placeholder="YYYY-MM-DD", id="to-date", value=date.today().strftime("%Y-%m-%d"))
                
                yield Button("Show Stats", id="show-stats")
                
                # Results area
                yield Static("", id="stats-status")
                yield Static("", id="stats-results", classes="results")
        
        yield Footer()
    
    def on_mount(self):
        """Initialize screen state when mounted."""
        self.selected_type = None
        self.selected_count = None
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses on stats screen."""
        button_id = event.button.id
        
        if button_id == "type-artists":
            self.selected_type = "artists"
            self.update_status("Selected type: Artists")
        elif button_id == "type-tracks":
            self.selected_type = "tracks"
            self.update_status("Selected type: Tracks")
        elif button_id == "count-10":
            self.selected_count = 10
            self.update_status("Selected count: Top 10")
        elif button_id == "count-25":
            self.selected_count = 25
            self.update_status("Selected count: Top 25")
        elif button_id == "count-100":
            self.selected_count = 100
            self.update_status("Selected count: Top 100")
        elif button_id == "show-stats":
            self.show_stats()
    
    def update_status(self, message: str):
        """Update the status display."""
        self.query_one("#stats-status").update(message)
    
    def update_results(self, results: str):
        """Update the results display."""
        self.query_one("#stats-results").update(results)
    
    def show_stats(self):
        """Show the requested statistics."""
        if not self.selected_type or not self.selected_count:
            self.update_status("Please select both a type and count first.")
            return
        
        try:
            from_date = datetime.strptime(self.query_one("#from-date").value, "%Y-%m-%d")
            to_date = datetime.strptime(self.query_one("#to-date").value, "%Y-%m-%d")
            
            if from_date > to_date:
                self.update_status("Error: From date must be before To date.")
                return
            
            self.update_status(f"Fetching {self.selected_type} statistics...")
            self.update_results("Loading...")
            
            # Start stats query in a background thread
            def stats_task():
                try:
                    results_text = ""
                    
                    if self.selected_type == "artists":
                        results = get_top_artists(self.selected_count, from_date, to_date)
                        
                        if not results:
                            results_text = "No results found."
                        else:
                            results_text = f"Top {self.selected_count} Artists from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}:\n\n"
                            for i, (artist, plays) in enumerate(results, 1):
                                results_text += f"{i}. {artist} ({plays} plays)\n"
                    
                    elif self.selected_type == "tracks":
                        results = get_top_tracks(self.selected_count, from_date, to_date)
                        
                        if not results:
                            results_text = "No results found."
                        else:
                            results_text = f"Top {self.selected_count} Tracks from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}:\n\n"
                            for i, (artist, title, plays) in enumerate(results, 1):
                                results_text += f"{i}. {artist} - {title} ({plays} plays)\n"
                    
                    # Update results when complete
                    self.app.call_from_thread(
                        self.update_results,
                        results_text
                    )
                    self.app.call_from_thread(
                        self.update_status,
                        "Statistics loaded successfully."
                    )
                except Exception as e:
                    # Update status with error
                    self.app.call_from_thread(
                        self.update_status,
                        f"Error fetching statistics: {str(e)}"
                    )
                    self.app.call_from_thread(
                        self.update_results,
                        ""
                    )
            
            threading.Thread(target=stats_task, daemon=True).start()
            
        except ValueError:
            self.update_status("Error: Invalid date format. Use YYYY-MM-DD.")
            self.update_results("")
    
    def action_go_back(self):
        """Handle the 'back' action."""
        self.app.pop_screen()

class StreamScreen(TaskScreen):
    """Screen for streaming GRRIF radio."""
    
    BINDINGS = [
        Binding("b", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for stream screen."""
        yield Header()
        
        with Container():
            yield Static("Stream GRRIF Radio", id="screen-title")
            
            with Vertical():
                yield Static("Select quality:")
                with Horizontal():
                    yield Button("High Quality MP3", id="quality-mp3-high", variant="primary")
                    yield Button("Low Quality MP3", id="quality-mp3-low", variant="primary")
                    yield Button("High Quality AAC", id="quality-aac-high", variant="primary")
                
                with Horizontal():
                    yield Button("Start Streaming", id="start-stream", variant="success")
                    yield Button("Stop Streaming", id="stop-stream", variant="error")
                
                yield Static("", id="stream-status")
                yield Static("", id="now-playing")
        
        yield Footer()
    
    def on_mount(self):
        """Initialize screen state when mounted."""
        self.selected_quality = "mp3_high"
        self.is_streaming = False
        self._stop_flag = threading.Event()
        self._scrobbler = None
        
        # Set default quality selection
        self.update_status("Selected quality: High Quality MP3")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses on stream screen."""
        button_id = event.button.id
        
        if button_id == "quality-mp3-high":
            self.selected_quality = "mp3_high"
            self.update_status("Selected quality: High Quality MP3")
        elif button_id == "quality-mp3-low":
            self.selected_quality = "mp3_low"
            self.update_status("Selected quality: Low Quality MP3")
        elif button_id == "quality-aac-high":
            self.selected_quality = "aac_high"
            self.update_status("Selected quality: High Quality AAC")
        elif button_id == "start-stream":
            self.start_streaming()
        elif button_id == "stop-stream":
            self.stop_streaming()
    
    def update_status(self, message: str):
        """Update the status display."""
        self.query_one("#stream-status").update(message)
    
    def update_now_playing(self, message: str):
        """Update the now playing display."""
        self.query_one("#now-playing").update(message)
    
    def start_streaming(self):
        """Start streaming GRRIF radio."""
        if self.is_streaming:
            self.update_status("Already streaming. Stop current stream first.")
            return
        
        self.update_status(f"Starting stream with {self.selected_quality}...")
        self.update_now_playing("Buffering...")
        
        # Clear stop flag
        self._stop_flag.clear()
        
        # Start streaming in a background thread
        def stream_task():
            try:
                # Initialize scrobbler
                self._scrobbler = TrackScrobbler()
                
                # Start track tracking thread
                track_thread = threading.Thread(
                    target=self._track_now_playing,
                    daemon=True
                )
                track_thread.start()
                
                # Start playback (blocking call, but in a separate thread)
                # This is a simplified version for the TUI - the actual implementation
                # would use the player module more directly
                from .grrif_player import start_playback
                start_playback(self.selected_quality)
                
                # Update status when stopped
                self.app.call_from_thread(
                    self.update_status,
                    "Streaming stopped."
                )
                self.app.call_from_thread(
                    self.update_now_playing,
                    ""
                )
                self.app.call_from_thread(
                    self._set_streaming_state,
                    False
                )
            except Exception as e:
                # Update status with error
                self.app.call_from_thread(
                    self.update_status,
                    f"Error during streaming: {str(e)}"
                )
                self.app.call_from_thread(
                    self.update_now_playing,
                    ""
                )
                self.app.call_from_thread(
                    self._set_streaming_state,
                    False
                )
        
        # Start thread
        self._stream_thread = threading.Thread(target=stream_task, daemon=True)
        self._stream_thread.start()
        
        # Update state
        self.is_streaming = True
    
    def _track_now_playing(self):
        """Track the currently playing song and update the display."""
        while not self._stop_flag.is_set():
            try:
                if self._scrobbler:
                    track_info = self._scrobbler.get_current_track()
                    
                    if track_info:
                        self.app.call_from_thread(
                            self.update_now_playing,
                            f"Now playing: {track_info['artist']} - {track_info['title']}"
                        )
            except Exception as e:
                logger.error(f"Error updating now playing: {e}")
            
            # Check every second
            time.sleep(1)
    
    def _set_streaming_state(self, is_streaming: bool):
        """Update the streaming state."""
        self.is_streaming = is_streaming
    
    def stop_streaming(self):
        """Stop streaming GRRIF radio."""
        if not self.is_streaming:
            self.update_status("Not currently streaming.")
            return
        
        self.update_status("Stopping stream...")
        
        # Set stop flag
        self._stop_flag.set()
        
        # Call stop_playback from the player module
        from .grrif_player import stop_playback
        stop_playback()
        
        # Update state
        self.is_streaming = False
        self.update_now_playing("")
        self.update_status("Streaming stopped.")
    
    def on_unmount(self):
        """Clean up when screen is unmounted."""
        self.stop_streaming()
    
    def action_go_back(self):
        """Handle the 'back' action."""
        self.stop_streaming()
        self.app.pop_screen()

class ScrobbleScreen(TaskScreen):
    """Screen for scrobbling to Last.fm."""
    
    BINDINGS = [
        Binding("b", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for scrobble screen."""
        yield Header()
        
        with Container():
            yield Static("Last.fm Scrobbling", id="screen-title")
            
            with Vertical():
                yield Static("Scrobbling Options:")
                with Horizontal():
                    yield Button("Start Scrobbling", id="start-scrobble", variant="success")
                    yield Button("Stop Scrobbling", id="stop-scrobble", variant="error")
                
                yield Static("", id="scrobble-status")
                yield Static("", id="now-playing")
                
                # Credentials info
                yield Static("\nLast.fm Credentials:", classes="section-title")
                yield Static("Configure credentials in the Settings screen", id="credentials-info")
        
        yield Footer()
    
    def on_mount(self):
        """Initialize screen state when mounted."""
        self.is_scrobbling = False
        self._stop_flag = threading.Event()
        self._scrobbler = None
        
        # Update credentials info
        self.update_credentials_info()
    
    def update_credentials_info(self):
        """Update the credentials info display."""
        config = Config()
        credentials = config.get_lastfm_credentials()
        
        if credentials['api_key'] and credentials['api_secret'] and credentials['session_key']:
            self.query_one("#credentials-info").update("Credentials are configured and ready to use.")
        else:
            self.query_one("#credentials-info").update("Credentials not configured. Please set them in the Settings screen.")
    
    def update_status(self, message: str):
        """Update the status display."""
        self.query_one("#scrobble-status").update(message)
    
    def update_now_playing(self, message: str):
        """Update the now playing display."""
        self.query_one("#now-playing").update(message)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses on scrobble screen."""
        button_id = event.button.id
        
        if button_id == "start-scrobble":
            self.start_scrobbling()
        elif button_id == "stop-scrobble":
            self.stop_scrobbling()
    
    def start_scrobbling(self):
        """Start scrobbling to Last.fm."""
        if self.is_scrobbling:
            self.update_status("Already scrobbling. Stop current session first.")
            return
        
        # Check credentials
        config = Config()
        credentials = config.get_lastfm_credentials()
        
        if not all([credentials['api_key'], credentials['api_secret'], credentials['session_key']]):
            self.update_status("Last.fm credentials not configured. Please set them in the Settings screen.")
            return
        
        self.update_status("Starting scrobbling...")
        self.update_now_playing("Waiting for track info...")
        
        # Clear stop flag
        self._stop_flag.clear()
        
        # Start scrobbling in a background thread
        def scrobble_task():
            try:
                # Initialize scrobbler
                self._scrobbler = TrackScrobbler()
                
                # Start tracking
                self._scrobbler.start_tracking(self._stop_flag)
                
                # Update status when stopped
                self.app.call_from_thread(
                    self.update_status,
                    "Scrobbling stopped."
                )
                self.app.call_from_thread(
                    self.update_now_playing,
                    ""
                )
                self.app.call_from_thread(
                    self._set_scrobbling_state,
                    False
                )
            except Exception as e:
                # Update status with error
                self.app.call_from_thread(
                    self.update_status,
                    f"Error during scrobbling: {str(e)}"
                )
                self.app.call_from_thread(
                    self.update_now_playing,
                    ""
                )
                self.app.call_from_thread(
                    self._set_scrobbling_state,
                    False
                )
        
        # Start thread for tracking now playing info
        def now_playing_tracker():
            while not self._stop_flag.is_set():
                try:
                    if self._scrobbler:
                        track_info = self._scrobbler.get_current_track()
                        
                        if track_info:
                            self.app.call_from_thread(
                                self.update_now_playing,
                                f"Now playing: {track_info['artist']} - {track_info['title']}"
                            )
                except Exception as e:
                    logger.error(f"Error updating now playing: {e}")
                
                # Check every second
                time.sleep(1)
        
        # Start threads
        self._scrobble_thread = threading.Thread(target=scrobble_task, daemon=True)
        self._scrobble_thread.start()
        
        self._now_playing_thread = threading.Thread(target=now_playing_tracker, daemon=True)
        self._now_playing_thread.start()
        
        # Update state
        self.is_scrobbling = True
        self.update_status("Scrobbling started. Tracks will be scrobbled to Last.fm.")
    
    def _set_scrobbling_state(self, is_scrobbling: bool):
        """Update the scrobbling state."""
        self.is_scrobbling = is_scrobbling
    
    def stop_scrobbling(self):
        """Stop scrobbling to Last.fm."""
        if not self.is_scrobbling:
            self.update_status("Not currently scrobbling.")
            return
        
        self.update_status("Stopping scrobbling...")
        
        # Set stop flag
        self._stop_flag.set()
        
        # Update state
        self.is_scrobbling = False
        self.update_now_playing("")
        self.update_status("Scrobbling stopped.")
    
    def on_unmount(self):
        """Clean up when screen is unmounted."""
        self.stop_scrobbling()
    
    def action_go_back(self):
        """Handle the 'back' action."""
        self.stop_scrobbling()
        self.app.pop_screen()

class SettingsScreen(Screen):
    """Screen for configuring GRRIF Tools."""
    
    BINDINGS = [
        Binding("b", "go_back", "Back"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for settings screen."""
        yield Header()
        
        with Container():
            yield Static("Settings", id="screen-title")
            
            # Last.fm Settings
            yield Static("Last.fm Credentials:", classes="section-title")
            
            with Vertical():
                with Horizontal():
                    yield Static("API Key:", classes="label")
                    yield Input(placeholder="Your Last.fm API Key", id="api-key")
                
                with Horizontal():
                    yield Static("API Secret:", classes="label")
                    yield Input(placeholder="Your Last.fm API Secret", id="api-secret")
                
                with Horizontal():
                    yield Static("Session Key:", classes="label")
                    yield Input(placeholder="Your Last.fm Session Key", id="session-key")
                
                yield Button("Save Credentials", id="save-credentials", variant="primary")
                
                yield Static("", id="settings-status")
                
                # Information about getting Last.fm credentials
                yield Static("\nHow to get Last.fm credentials:", classes="section-title")
                yield Static("1. Create an API account at https://www.last.fm/api/account/create")
                yield Static("2. Get your API key and secret")
                yield Static("3. Follow the authentication protocol at https://www.last.fm/api/authspec to obtain a session key")
        
        yield Footer()
    
    def on_mount(self):
        """Load existing settings when screen is mounted."""
        config = Config()
        credentials = config.get_lastfm_credentials()
        
        # Load existing credentials if available
        if credentials['api_key']:
            self.query_one("#api-key").value = credentials['api_key']
        
        if credentials['api_secret']:
            self.query_one("#api-secret").value = credentials['api_secret']
        
        if credentials['session_key']:
            self.query_one("#session-key").value = credentials['session_key']
    
    def update_status(self, message: str):
        """Update the status display."""
        self.query_one("#settings-status").update(message)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses on settings screen."""
        button_id = event.button.id
        
        if button_id == "save-credentials":
            self.save_credentials()
    
    def save_credentials(self):
        """Save Last.fm credentials."""
        api_key = self.query_one("#api-key").value
        api_secret = self.query_one("#api-secret").value
        session_key = self.query_one("#session-key").value
        
        if not (api_key and api_secret and session_key):
            self.update_status("Error: All fields are required.")
            return
        
        try:
            config = Config()
            config.set_lastfm_credentials(api_key, api_secret, session_key)
            self.update_status("Credentials saved successfully.")
        except Exception as e:
            self.update_status(f"Error saving credentials: {str(e)}")
    
    def action_go_back(self):
        """Handle the 'back' action."""
        self.app.pop_screen()

def create_css_file():
    """Create the CSS file for the TUI if it doesn't exist."""
    from pathlib import Path
    
    # CSS content
    css_content = """/* CSS for the GRRIF Tools TUI */
Screen {
    background: #0f0f0f;
    color: #ffffff;
}

#main {
    width: 100%;
    height: 100%;
    padding: 1 2;
}

#welcome {
    width: 100%;
    height: auto;
    content-align: center middle;
    text-align: center;
    margin: 2 0;
}

#screen-title {
    text-style: bold;
    width: 100%;
    text-align: center;
    margin: 1 0;
}

#buttons {
    width: 100%;
    height: auto;
    align: center top;
    margin: 1 0;
}

Button {
    margin: 0 1;
}

.label {
    padding: 1 1;
    width: auto;
}

Input {
    width: 30;
}

.section-title {
    text-style: bold;
    margin-top: 1;
}

.results {
    height: auto;
    max-height: 20;
    overflow: auto;
    border: solid gray;
    padding: 1;
    margin-top: 1;
}

Footer {
    background: #2e2e2e;
}
"""
    
    # Write CSS file to the package directory
    import os
    package_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(package_dir, "grrif.css")
    
    if not os.path.exists(css_path):
        with open(css_path, "w") as f:
            f.write(css_content)

def run_tui():
    """Run the TUI application."""
    create_css_file()
    
    # Run the app
    app = GRRIFApp()
    app.run()