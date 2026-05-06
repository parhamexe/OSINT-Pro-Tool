"""
Simple SQLite database for search history
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = "osint_history.db"

def init_database():
    """Initialize database if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS searches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        identifier TEXT NOT NULL,
        platform TEXT NOT NULL,
        success INTEGER,
        message TEXT,
        data TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def save_search_result(result):
    """Save a search result to database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO searches (timestamp, identifier, platform, success, message, data)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        result.get("data", {}).get("username") or result.get("data", {}).get("phone") or result.get("data", {}).get("name", "unknown"),
        result.get("data", {}).get("platform", "unknown"),
        1 if result.get("success") else 0,
        result.get("message", ""),
        str(result.get("data", {}))
    ))
    
    conn.commit()
    conn.close()

def get_search_history(limit=50):
    """Retrieve recent search history"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM searches 
    ORDER BY timestamp DESC 
    LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize on import
init_database()
