"""
GRRIF Player helper functions.

This module provides functions to stream GRRIF radio to the console.
"""
import os
import threading
import time
from pathlib import Path
from typing import Optional
import requests
import miniaudio

from .utils import get_buffer_path, logger
from .grrif_scrobbler import TrackScrobbler

# Global state variables (will be replaced with a singleton class in a full implementation)
_player_thread = None
_stream_thread = None
_stop_event = None
_scrobbler = None

def stream_and_write(url: str, file_path: Path, max_size: int, stop_event: threading.Event) -> None:
    """
    Stream audio from URL and write to a buffer file.
    
    Args:
        url: The streaming URL.
        file_path: Path to the buffer file.
        max_size: Maximum buffer size in bytes.
        stop_event: Event to signal when to stop streaming.
    """
    try:
        headers = {
            'User-Agent': 'GRRIFTools/1.0',  # Add a user agent to help with stream reliability
        }
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()  # Raise for HTTP errors
        
        with open(file_path, 'wb') as file:
            buffer = bytearray()
            current_size = 0
            
            for chunk in response.iter_content(chunk_size=1024):
                if stop_event.is_set():
                    break
                    
                buffer.extend(chunk)
                current_size += len(chunk)
                
                # Keep buffer at a reasonable size by removing oldest data
                while current_size > max_size:
                    buffer.pop(0)
                    current_size -= 1
                
                file.write(chunk)
                file.flush()
                
        logger.info("Streaming thread stopped")
    except requests.RequestException as e:
        logger.error(f"Error streaming from URL: {e}")
        stop_event.set()  # Signal other threads to stop

def play_stream(file_path: Path, stop_event: threading.Event) -> None:
    """
    Play audio from a buffer file.
    
    Args:
        file_path: Path to the buffer file.
        stop_event: Event to signal when to stop playback.
    """
    logger.info("Buffering audio...")
    buffer_time = 3  # seconds
    
    # Wait for buffer to fill
    time.sleep(buffer_time)
    
    try:
        # Start the scrobbler in a separate thread
        global _scrobbler
        _scrobbler = TrackScrobbler()
        
        # Check if scrobbler has credentials before starting
        if _scrobbler.has_credentials():
            logger.info("Last.fm credentials found, scrobbling enabled")
            scrobbler_thread = threading.Thread(
                target=_scrobbler.start_tracking, 
                args=(stop_event,)
            )
            scrobbler_thread.daemon = True  # Thread will terminate when program exits
            scrobbler_thread.start()
        else:
            logger.warning("Last.fm credentials not found, scrobbling disabled")
            print("Note: Last.fm scrobbling is disabled. To enable, please set up your credentials.")
            print("You can either:")
            print("1. Use 'grrif_tools scrobble settings' to configure via CLI")
            print("2. Create a grrif_secrets.py file with API_KEY, API_SECRET, and SESSION_KEY variables")
        
        # Start playback
        logger.info("Starting playback...")
        
        # Keep playing flag
        playing = True
        
        try:
            # Use a context manager for the device
            with miniaudio.PlaybackDevice() as device:
                # Initial stream
                stream = miniaudio.stream_file(str(file_path))
                device.start(stream)
                
                # Keep playing until stopped
                while not stop_event.is_set() and playing:
                    # Sleep to avoid consuming too much CPU
                    time.sleep(0.5)
                    
                    # Try to check if we need to restart the stream
                    try:
                        # Print currently playing track from scrobbler
                        if _scrobbler and _scrobbler.current_track:
                            track = _scrobbler.current_track
                            print(f"\rNow playing: {track['artist']} - {track['title']}   ", end="", flush=True)
                    except Exception as e:
                        # If any error occurs, try to restart the stream
                        logger.warning(f"Playback issue, attempting restart: {e}")
                        try:
                            device.stop()
                            stream = miniaudio.stream_file(str(file_path))
                            device.start(stream)
                        except Exception as restart_error:
                            logger.error(f"Error restarting stream: {restart_error}")
                            playing = False  # Stop the loop if we can't restart
                
                # Stop playback
                device.stop()
                
        except miniaudio.DecodeError as e:
            logger.error(f"Error decoding audio: {e}")
        except Exception as e:
            logger.error(f"Playback error: {e}")
        
        logger.info("Playback stopped")
    except Exception as e:
        logger.error(f"Error in playback thread: {e}")
    finally:
        # Ensure stop event is set to signal other threads
        stop_event.set()

def start_playback(quality: str = "mp3_high") -> None:
    """
    Start streaming and playing GRRIF radio.
    
    Args:
        quality: The streaming quality, one of 'mp3_high', 'mp3_low', or 'aac_high'.
    """
    global _player_thread, _stream_thread, _stop_event
    
    # Check if already playing
    if _player_thread and _player_thread.is_alive():
        logger.warning("Already streaming. Stop current stream before starting a new one.")
        return
    
    # Create a new stop event
    _stop_event = threading.Event()
    
    # Get stream URL based on quality
    if quality == "mp3_high":
        url = "https://grrif.ice.infomaniak.ch/grrif-high.mp3"
    elif quality == "mp3_low":
        url = "https://grrif.ice.infomaniak.ch/grrif-48.mp3"
    elif quality == "aac_high":
        url = "https://grrif.ice.infomaniak.ch/grrif-128.aac"
    else:
        logger.error(f"Unknown quality: {quality}")
        return
    
    # Path to buffer file in user data directory
    buffer_file = get_buffer_path()
    
    # Set buffer size (500 KB - increased for better streaming)
    max_file_size = 500 * 1024
    
    # Create an empty buffer file if it doesn't exist
    if not buffer_file.exists():
        buffer_file.touch()
    
    # Start streaming thread
    _stream_thread = threading.Thread(
        target=stream_and_write, 
        args=(url, buffer_file, max_file_size, _stop_event)
    )
    _stream_thread.daemon = True
    _stream_thread.start()
    
    # Start playback thread
    _player_thread = threading.Thread(
        target=play_stream, 
        args=(buffer_file, _stop_event)
    )
    _player_thread.daemon = True
    _player_thread.start()
    
    logger.info(f"Streaming GRRIF ({quality}) started")
    
    try:
        # Keep main thread alive until user presses Enter
        print("\nStreaming. Press Enter to stop...\n")
        input()  # Wait for Enter key
        logger.info("User requested stop")
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        stop_playback()

def stop_playback() -> None:
    """Stop the currently playing stream."""
    global _stop_event
    
    if _stop_event:
        # Signal threads to stop
        _stop_event.set()
        
        logger.info("Stopping playback, please wait...")
        
        # Wait for threads to finish (with timeout)
        if _stream_thread:
            _stream_thread.join(timeout=10)
        if _player_thread:
            _player_thread.join(timeout=10)
        
        # Remove buffer file
        buffer_file = get_buffer_path()
        if buffer_file.exists():
            try:
                os.remove(buffer_file)
                logger.info("Buffer file removed")
            except OSError as e:
                logger.error(f"Error removing buffer file: {e}")
        
        logger.info("Playback stopped")