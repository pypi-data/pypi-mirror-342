"""
GRRIF Scrobbler helper functions.

This module provides functions to scrobble GRRIF tracks to Last.fm.
"""
import time
import hashlib
import threading
import urllib.parse
import webbrowser
from typing import Dict, Optional, Any, List, Tuple
import requests
import titlecase

from .utils import Config, logger, get_lastfm_credentials

def authenticate_lastfm(api_key: str, api_secret: str) -> dict:
    """
    Authenticate with Last.fm and obtain a session key.
    
    This function handles the complete Last.fm authentication flow:
    1. Requests an authentication token
    2. Prompts the user to authorize the token on Last.fm's website
    3. Waits for authorization and requests a session key
    
    Args:
        api_key: Your Last.fm API key
        api_secret: Your Last.fm API secret
        
    Returns:
        A dictionary containing the session key and username if successful,
        or error information if unsuccessful.
    """
    # Step 1: Get a request token
    try:
        token_url = f"http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={api_key}&format=json"
        response = requests.get(token_url)
        response.raise_for_status()
        
        data = response.json()
        if 'error' in data:
            return {'error': data['error'], 'message': data['message']}
        
        token = data['token']
        print(f"Obtained request token: {token}")
        
        # Step 2: Redirect user to authorization page
        auth_url = f"https://www.last.fm/api/auth?api_key={api_key}&token={token}"
        print(f"\nPlease authorize this application by visiting:")
        print(f"{auth_url}")
        
        # Try to open the browser automatically
        try:
            webbrowser.open(auth_url)
            print("\nA browser window should have opened. If not, please copy and paste the URL manually.")
        except:
            print("\nUnable to open browser automatically. Please copy and paste the URL into your browser.")
        
        # Step 3: Wait for user confirmation and get session key
        input("\nAfter authorizing the application on Last.fm, press Enter to continue...")
        
        # Create API signature for auth.getSession
        string_to_hash = f"api_key{api_key}methodauth.getSessiontoken{token}{api_secret}"
        api_sig = hashlib.md5(string_to_hash.encode('utf-8')).hexdigest()
        
        # Request session key
        session_url = f"https://ws.audioscrobbler.com/2.0/?method=auth.getSession&api_key={api_key}&token={token}&api_sig={api_sig}&format=json"
        session_response = requests.get(session_url)
        session_response.raise_for_status()
        
        session_data = session_response.json()
        if 'error' in session_data:
            return {'error': session_data['error'], 'message': session_data['message']}
        
        session_key = session_data['session']['key']
        username = session_data['session']['name']
        
        return {
            'success': True,
            'session_key': session_key,
            'username': username
        }
    
    except requests.RequestException as e:
        return {'error': 'network_error', 'message': str(e)}
    except ValueError as e:
        return {'error': 'json_parse_error', 'message': str(e)}
    except KeyError as e:
        return {'error': 'missing_field', 'message': f"Missing field in response: {str(e)}"}
    except Exception as e:
        return {'error': 'unknown_error', 'message': str(e)}

class TrackScrobbler:
    """
    Class to handle scrobbling tracks to Last.fm.
    """
    def __init__(self):
        """Initialize the scrobbler with configuration and state."""
        self.credentials = get_lastfm_credentials()
        self.current_track = None
        self.last_check_time = ""
        self.check_interval = 60  # Check for new track every 60 seconds
        self.last_scrobbled_track = None  # Store info about the last scrobbled track
        
    def has_credentials(self) -> bool:
        """Check if the required Last.fm credentials are set."""
        return all([
            self.credentials.get('api_key'),
            self.credentials.get('api_secret'),
            self.credentials.get('session_key')
        ])
    
    def hash_request(self, params: Dict[str, str]) -> str:
        """
        Create a hash for Last.fm API authentication.
        
        Args:
            params: The parameters to hash.
            
        Returns:
            The md5 hash of the parameters and API secret.
        """
        items = sorted(params.keys())
        string = ''
        
        for item in items:
            if item == 'format' or item == 'callback':
                continue  # Skip these parameters as per Last.fm API docs
            string += item + params[item]
            
        string += self.credentials['api_secret']
        
        # Create MD5 hash
        return hashlib.md5(string.encode('utf8')).hexdigest()
    
    def scrobble_track(self, artist: str, title: str, timestamp: int) -> bool:
        """
        Scrobble a track to Last.fm.
        
        Args:
            artist: The artist name.
            title: The track title.
            timestamp: The Unix timestamp when the track started playing.
            
        Returns:
            True if scrobbling was successful, False otherwise.
        """
        if not self.has_credentials():
            logger.warning("Cannot scrobble: Last.fm credentials not set")
            return False
        
        # Avoid duplicate scrobbles for the same track in quick succession
        if self.last_scrobbled_track:
            last_artist, last_title, last_time = self.last_scrobbled_track
            if (last_artist == artist and 
                last_title == title and 
                abs(last_time - timestamp) < 300):  # Within 5 minutes
                logger.info(f"Skipping duplicate scrobble for: {artist} - {title}")
                return True
            
        url = "https://ws.audioscrobbler.com/2.0/"
        
        params = {
            "method": "track.scrobble",
            "api_key": self.credentials['api_key'],
            "artist": artist,
            "track": title,
            "timestamp": str(timestamp),
            "chosenByUser": "0",
            "format": "json",
            "sk": self.credentials['session_key'],
        }
        
        # Generate API signature
        api_sig = self.hash_request(params)
        params["api_sig"] = api_sig
        
        try:
            # Properly encode parameters
            response = requests.post(url, data=params)
            
            # Check if request was successful
            if response.status_code == 200:
                response_data = response.json()
                if 'error' in response_data:
                    error_code = response_data.get('error')
                    error_message = response_data.get('message', 'Unknown error')
                    logger.error(f"Last.fm API error {error_code}: {error_message}")
                    return False
                
                logger.info(f"Successfully scrobbled: {artist} - {title}")
                self.last_scrobbled_track = (artist, title, timestamp)
                return True
            else:
                logger.error(f"Failed to scrobble track (HTTP {response.status_code}): {response.text}")
                return False
        except requests.RequestException as e:
            logger.error(f"Network error during scrobbling: {e}")
            return False
        except ValueError as e:
            logger.error(f"Error parsing Last.fm API response: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during scrobbling: {e}")
            return False
    
    def now_playing(self, artist: str, title: str) -> bool:
        """
        Send now playing notification to Last.fm.
        
        Args:
            artist: The artist name.
            title: The track title.
            
        Returns:
            True if notification was successful, False otherwise.
        """
        if not self.has_credentials():
            logger.warning("Cannot update now playing: Last.fm credentials not set")
            return False
            
        url = "https://ws.audioscrobbler.com/2.0/"
        
        params = {
            "method": "track.updateNowPlaying",
            "api_key": self.credentials['api_key'],
            "artist": artist,
            "track": title,
            "format": "json",
            "sk": self.credentials['session_key'],
        }
        
        # Generate API signature
        api_sig = self.hash_request(params)
        params["api_sig"] = api_sig
        
        try:
            response = requests.post(url, data=params)
            
            if response.status_code == 200:
                response_data = response.json()
                if 'error' in response_data:
                    error_code = response_data.get('error')
                    error_message = response_data.get('message', 'Unknown error')
                    logger.error(f"Last.fm API error {error_code}: {error_message}")
                    return False
                
                logger.info(f"Updated now playing: {artist} - {title}")
                return True
            else:
                logger.error(f"Failed to update now playing (HTTP {response.status_code}): {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error updating now playing: {e}")
            return False
    
    def get_current_track(self) -> Optional[Dict[str, str]]:
        """
        Get the currently playing track from GRRIF.
        
        Returns:
            A dictionary with track information or None if failed.
        """
        try:
            # Add a cache buster to avoid caching issues
            cache_buster = int(time.time())
            url = f"https://www.grrif.ch/live/covers.json?_={cache_buster}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # GRRIF API structure can change, so let's be careful
            if not isinstance(data, list) or len(data) < 4:
                logger.warning("Unexpected GRRIF API response format")
                return None
            
            current_track_data = data[3]  # The current track is typically at index 3
            
            # Handle case where fields might be empty or missing
            artist = current_track_data.get("Artist", "").strip()
            title = current_track_data.get("Title", "").strip()
            time_str = current_track_data.get("Hours", "").strip()
            
            if not artist or not title:
                logger.warning(f"Incomplete track data: Artist='{artist}', Title='{title}'")
                return None
                
            return {
                "artist": titlecase.titlecase(artist),
                "title": titlecase.titlecase(title),
                "time": time_str
            }
        except requests.Timeout:
            logger.error("Timeout while fetching current track from GRRIF")
            return None
        except requests.RequestException as e:
            logger.error(f"Network error retrieving current track: {e}")
            return None
        except ValueError as e:
            logger.error(f"Error parsing GRRIF JSON response: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Unexpected GRRIF API response structure: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting current track: {e}")
            return None
    
    def start_tracking(self, stop_event: threading.Event) -> None:
        """
        Start tracking the currently playing track and scrobble it.
        
        Args:
            stop_event: Event to signal when to stop tracking.
        """
        logger.info("Starting track tracking")
        
        if not self.has_credentials():
            logger.error("Cannot start tracking: Last.fm credentials not set")
            return
            
        while not stop_event.is_set():
            try:
                track_info = self.get_current_track()
                
                if track_info:
                    # Update current track info for other threads to access
                    if track_info["time"] != self.last_check_time:
                        # New track detected
                        self.current_track = track_info
                        self.last_check_time = track_info["time"]
                        
                        # Log the currently playing track
                        logger.info(f"Now playing: {track_info['artist']} - {track_info['title']}")
                        
                        # Update now playing status
                        self.now_playing(track_info["artist"], track_info["title"])
                        
                        # Scrobble the track with a timestamp 30 seconds in the past
                        # This ensures the track is scrobbled correctly
                        timestamp = int(time.time() - 30)
                        
                        # Make multiple attempts to scrobble if needed
                        scrobble_success = False
                        for attempt in range(3):
                            if stop_event.is_set():
                                break
                                
                            scrobble_success = self.scrobble_track(
                                track_info["artist"], 
                                track_info["title"], 
                                timestamp
                            )
                            
                            if scrobble_success:
                                break
                                
                            logger.warning(f"Scrobble attempt {attempt+1} failed, retrying in 5 seconds...")
                            time.sleep(5)
                        
                        if not scrobble_success:
                            logger.error(f"Failed to scrobble after multiple attempts: {track_info['artist']} - {track_info['title']}")
            except Exception as e:
                logger.error(f"Error in track tracking loop: {e}")
            
            # Check for new track after interval, but poll the stop event more frequently
            for _ in range(self.check_interval):
                if stop_event.is_set():
                    break
                time.sleep(1)
        
        logger.info("Track tracking stopped")

def start_scrobbling(stream_mode: str = "0") -> None:
    """
    Start standalone scrobbling mode.
    
    Args:
        stream_mode: "0" for standalone mode.
    """
    stop_event = threading.Event()
    
    try:
        scrobbler = TrackScrobbler()
        
        if not scrobbler.has_credentials():
            print("Last.fm credentials not set.")
            print("Please either:")
            print("1. Use 'grrif_tools scrobble authenticate' to set up authentication")
            print("2. Use 'grrif_tools scrobble settings' to configure via CLI")
            print("3. Create a grrif_secrets.py file with API_KEY, API_SECRET, and SESSION_KEY variables")
            return
            
        print("Starting scrobbling to Last.fm. Press Ctrl+C to stop.")
        print("Listening for tracks from GRRIF...")
        
        # Start scrobbling in the main thread
        scrobbler.start_tracking(stop_event)
    except KeyboardInterrupt:
        print("\nScrobbling stopped by user.")
    finally:
        stop_event.set()

def stop_scrobbling() -> None:
    """Placeholder for stopping scrobbling in the TUI."""
    # In the TUI implementation, this will be used to stop scrobbling
    pass