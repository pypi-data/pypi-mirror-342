"""
GRRIF Archiver helper functions.

This module provides functions to archive GRRIF's play history
to different destinations like a SQLite database or text files.
"""
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any
import requests
import titlecase
from bs4 import BeautifulSoup

from .utils import get_database_path, get_plays_dir, logger

def scrape_plays(base_url: str, date_str: str) -> List[Dict[str, str]]:
    """
    Scrape plays from GRRIF website for a specific date.
    
    Args:
        base_url: The base URL to scrape from.
        date_str: The date string in YYYY-MM-DD format.
    
    Returns:
        A list of dictionaries containing play information.
    """
    url = base_url.format(date_str)
    logger.info(f"Scraping plays from {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.content, "html.parser")
        data_section = soup.find("div", {"class": "listing-search-titres"})
        
        if not data_section:
            logger.warning(f"No data section found for {date_str}")
            return []
            
        data_items = data_section.find_all("article")
        plays = []
        
        for item in data_items:
            try:
                playtime = item.find("div", {"class": "hours"}).text.strip()
                artist = item.find("div", {"class": "artist"}).text.strip()
                title = item.find("div", {"class": "title"}).text.strip()
                
                # Prettify the data
                pretty_artist = titlecase.titlecase(artist)
                pretty_title = titlecase.titlecase(title)
                
                plays.append({
                    "date": date_str,
                    "time": playtime,
                    "artist": pretty_artist,
                    "title": pretty_title
                })
            except AttributeError as e:
                logger.error(f"Error parsing play item: {e}")
                continue
                
        return plays
        
    except requests.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return []

def setup_database() -> Path:
    """
    Set up the SQLite database for storing plays.
    
    Returns:
        The path to the database file.
    """
    database_path = get_database_path()
    
    # Create an empty db if it does not exist yet
    if not database_path.exists():
        logger.info(f"Creating new database at {database_path}")
        
        conn = sqlite3.connect(database_path)
        conn.execute(
            """CREATE TABLE plays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            time TIME NOT NULL,
            artist TEXT NOT NULL,
            title TEXT NOT NULL,
            CONSTRAINT unique_play UNIQUE (date, time)
            );
        """
        )
        conn.commit()
        conn.close()
    
    logger.info(f"Database loaded at {database_path}")
    return database_path

def plays_to_db(base_url: str, start_date: datetime, end_date: datetime) -> None:
    """
    Scrape plays and store them in a SQLite database.
    
    Args:
        base_url: The base URL to scrape from.
        start_date: The start date.
        end_date: The end date.
    """
    database_path = setup_database()
    
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        plays = scrape_plays(base_url, date_str)
        
        for play in plays:
            try:
                c.execute(
                    "INSERT INTO plays (date, time, artist, title) VALUES (?, ?, ?, ?)",
                    (play["date"], play["time"], play["artist"], play["title"])
                )
                conn.commit()
            except sqlite3.IntegrityError:
                # Skip records that already exist
                pass
        
        logger.info(f"Plays for {date_str} saved to database")
        
        # Wait before next request to be nice to the server
        time.sleep(2)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    conn.close()
    logger.info(f"Data archived to {database_path} successfully!")

def plays_to_txt(base_url: str, start_date: datetime, end_date: datetime) -> None:
    """
    Scrape plays and store them in text files.
    
    Args:
        base_url: The base URL to scrape from.
        start_date: The start date.
        end_date: The end date.
    """
    plays_path = get_plays_dir()
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        plays = scrape_plays(base_url, date_str)
        
        if plays:
            # Create the YYYY/MM/ directory structure
            year_dir = plays_path / current_date.strftime("%Y")
            month_dir = year_dir / current_date.strftime("%m")
            month_dir.mkdir(parents=True, exist_ok=True)
            
            # Write to the DD.txt file
            file_path = month_dir / f"{current_date.strftime('%d')}.txt"
            
            with open(file_path, "w") as f:
                for play in reversed(plays):  # Reverse to get chronological order
                    f.write(f"{play['artist']} - {play['title']} (@{play['time']})\n")
            
            logger.info(f"Plays for {date_str} saved to {file_path}")
        
        # Wait before next request to be nice to the server
        time.sleep(2)
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    logger.info(f"Data archived to {plays_path} successfully!")

def plays_to_stdout(base_url: str, start_date: datetime, end_date: datetime) -> None:
    """
    Scrape plays and print them to stdout.
    
    Args:
        base_url: The base URL to scrape from.
        start_date: The start date.
        end_date: The end date.
    """
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        plays = scrape_plays(base_url, date_str)
        
        for play in reversed(plays):  # Reverse to get chronological order
            print(f"{play['artist']} - {play['title']} (@{play['time']} on {date_str})")
        
        # Wait before next request to be nice to the server
        time.sleep(2)
        
        # Move to the next day
        current_date += timedelta(days=1)