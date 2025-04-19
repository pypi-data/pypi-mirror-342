"""
GRRIF Stats helper functions.

This module provides functions to compute statistics from the GRRIF play history.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Tuple

from .utils import get_database_path, logger

def get_top_artists(limit: int, start_date: datetime, end_date: datetime) -> List[Tuple[str, int]]:
    """
    Get the top artists from the play history.
    
    Args:
        limit: The number of artists to return.
        start_date: The start date for the statistics.
        end_date: The end date for the statistics.
        
    Returns:
        A list of tuples containing (artist_name, play_count).
    """
    return _get_top_items("artist", limit, start_date, end_date)

def get_top_tracks(limit: int, start_date: datetime, end_date: datetime) -> List[Tuple[str, str, int]]:
    """
    Get the top tracks from the play history.
    
    Args:
        limit: The number of tracks to return.
        start_date: The start date for the statistics.
        end_date: The end date for the statistics.
        
    Returns:
        A list of tuples containing (artist_name, track_title, play_count).
    """
    conn = sqlite3.connect(get_database_path())
    conn.row_factory = sqlite3.Row
    
    query = """
    SELECT artist, title, COUNT(*) as plays
    FROM plays
    WHERE date BETWEEN ? AND ?
    GROUP BY artist, title
    ORDER BY plays DESC
    LIMIT ?
    """
    
    params = (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        limit
    )
    
    try:
        results = conn.execute(query, params).fetchall()
        # Convert to list of tuples
        return [(row["artist"], row["title"], row["plays"]) for row in results]
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return []
    finally:
        conn.close()

def _get_top_items(category: str, limit: int, start_date: datetime, end_date: datetime) -> List[Tuple[str, int]]:
    """
    Helper function to get top items from a specific category.
    
    Args:
        category: The category to get statistics for ('artist' or 'title').
        limit: The number of items to return.
        start_date: The start date for the statistics.
        end_date: The end date for the statistics.
        
    Returns:
        A list of tuples containing (item_name, play_count).
    """
    if category not in ["artist", "title"]:
        logger.error(f"Invalid category: {category}")
        return []
    
    conn = sqlite3.connect(get_database_path())
    conn.row_factory = sqlite3.Row
    
    query = f"""
    SELECT {category}, COUNT(*) as plays
    FROM plays
    WHERE date BETWEEN ? AND ?
    GROUP BY {category}
    ORDER BY plays DESC
    LIMIT ?
    """
    
    params = (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        limit
    )
    
    try:
        results = conn.execute(query, params).fetchall()
        # Convert to list of tuples
        return [(row[category], row["plays"]) for row in results]
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return []
    finally:
        conn.close()