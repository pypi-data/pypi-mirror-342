"""
Common utilities for GRRIF Tools.

This module provides utilities for file paths, configuration, and logging.
"""
import os
import logging
import importlib.util
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Union
import configparser

# Set up logging
logger = logging.getLogger("grrif_tools")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create user data directory
def get_user_data_dir() -> Path:
    """Get the user data directory for storing GRRIF Tools data."""
    data_dir = Path.home() / "grrif_data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

# Get database path
def get_database_path() -> Path:
    """Get the path to the SQLite database."""
    return get_user_data_dir() / "grrif_data.db"

# Get plays directory path
def get_plays_dir() -> Path:
    """Get the directory for storing play history text files."""
    plays_dir = get_user_data_dir() / "plays"
    plays_dir.mkdir(exist_ok=True)
    return plays_dir

# Get config path
def get_config_path() -> Path:
    """Get the path to the configuration file."""
    return get_user_data_dir() / "config.json"

# Get secrets module path
def get_secrets_path() -> Path:
    """Get the path to the grrif_secrets.py file."""
    # First check in user's home directory
    home_path = Path.home() / "grrif_secrets.py"
    if home_path.exists():
        return home_path
    
    # Then check in current directory
    current_path = Path.cwd() / "grrif_secrets.py"
    if current_path.exists():
        return current_path
    
    # Then check in user data directory
    data_path = get_user_data_dir() / "grrif_secrets.py"
    if data_path.exists():
        return data_path
    
    return None

# Get buffer file path
def get_buffer_path() -> Path:
    """Get the path to the audio buffer file."""
    return get_user_data_dir() / "buffer.mp3"

# Load secrets from Python module
def load_secrets_from_module() -> Optional[Dict[str, str]]:
    """Load Last.fm credentials from the grrif_secrets.py module."""
    secrets_path = get_secrets_path()
    
    if not secrets_path:
        return None
    
    try:
        # Load the module dynamically
        spec = importlib.util.spec_from_file_location("grrif_secrets", secrets_path)
        secrets_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(secrets_module)
        
        # Check if the module has the required variables
        api_key = getattr(secrets_module, 'API_KEY', None)
        api_secret = getattr(secrets_module, 'API_SECRET', None)
        session_key = getattr(secrets_module, 'SESSION_KEY', None)
        
        if api_key and api_secret and session_key:
            return {
                'api_key': api_key,
                'api_secret': api_secret,
                'session_key': session_key
            }
        else:
            logger.warning("grrif_secrets.py found but missing one or more required variables (API_KEY, API_SECRET, SESSION_KEY)")
            return None
    except Exception as e:
        logger.error(f"Error loading grrif_secrets.py: {e}")
        return None

# Config management class
class Config:
    """Configuration manager for GRRIF Tools."""
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Load configuration from JSON file."""
        config_path = get_config_path()
        
        # Set default configuration
        self._config = {
            'lastfm': {
                'api_key': '',
                'api_secret': '',
                'session_key': ''
            },
            'general': {
                'default_start_date': '2021-01-01'
            }
        }
        
        # Load existing configuration if it exists
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded_config = json.load(f)
                    
                # Update the default config with loaded values, preserving structure
                for section, values in loaded_config.items():
                    if section not in self._config:
                        self._config[section] = {}
                    
                    if isinstance(values, dict):
                        for key, value in values.items():
                            self._config[section][key] = value
                    else:
                        # Handle case where a section might be a non-dict
                        self._config[section] = values
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing config file: {e}. Using default configuration.")
            except Exception as e:
                logger.error(f"Error loading config file: {e}. Using default configuration.")
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Get a configuration value."""
        if section in self._config and key in self._config[section]:
            return self._config[section][key]
        return fallback
    
    def set(self, section: str, key: str, value: str) -> None:
        """Set a configuration value."""
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self._save_config()
    
    def _save_config(self) -> None:
        """Save configuration to JSON file."""
        try:
            with open(get_config_path(), 'w') as f:
                json.dump(self._config, f, indent=4)
            logger.debug("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            
    def get_lastfm_credentials(self) -> Dict[str, str]:
        """Get Last.fm API credentials."""
        # First try to load from secrets module
        secrets = load_secrets_from_module()
        if secrets:
            logger.info("Loaded Last.fm credentials from grrif_secrets.py")
            return secrets
        
        # Fall back to config file
        return {
            'api_key': self.get('lastfm', 'api_key', ''),
            'api_secret': self.get('lastfm', 'api_secret', ''),
            'session_key': self.get('lastfm', 'session_key', '')
        }
    
    def set_lastfm_credentials(self, api_key: str, api_secret: str, session_key: str) -> None:
        """Set Last.fm API credentials."""
        self.set('lastfm', 'api_key', api_key)
        self.set('lastfm', 'api_secret', api_secret)
        self.set('lastfm', 'session_key', session_key)

# Function to get Last.fm credentials from any source
def get_lastfm_credentials() -> Dict[str, str]:
    """
    Get Last.fm credentials from the most appropriate source.
    First tries grrif_secrets.py, then falls back to config.json.
    """
    # Try to load from secrets module first
    secrets = load_secrets_from_module()
    if secrets:
        return secrets
    
    # Fall back to config file
    config = Config()
    return config.get_lastfm_credentials()