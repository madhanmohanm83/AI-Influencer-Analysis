
import sqlite3
from pathlib import Path

from config import DATABASE_PATH


def get_connection():
    """Create and return a SQLite database connection."""

    database_file = Path(DATABASE_PATH)
    database_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(database_file)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create project database tables if they do not exist."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creators (
                channel_id TEXT PRIMARY KEY,
                channel_name TEXT NOT NULL,
                description TEXT,
                country TEXT,
                subscribers INTEGER DEFAULT 0,
                total_views INTEGER DEFAULT 0,
                total_videos INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                results_count INTEGER DEFAULT 0,
                searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL,
                brand_keyword TEXT NOT NULL,
                suitability_score REAL,
                rank INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (channel_id)
                    REFERENCES creators(channel_id)
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_creators(creators):
    """Insert or update creator records."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        for creator in creators:
            cursor.execute("""
                INSERT INTO creators (
                    channel_id,
                    channel_name,
                    description,
                    country,
                    subscribers,
                    total_views,
                    total_videos,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)

                ON CONFLICT(channel_id) DO UPDATE SET
                    channel_name = excluded.channel_name,
                    description = excluded.description,
                    country = excluded.country,
                    subscribers = excluded.subscribers,
                    total_views = excluded.total_views,
                    total_videos = excluded.total_videos,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                creator.get("channel_id"),
                creator.get("channel_name", "Unknown"),
                creator.get("description", ""),
                creator.get("country", "Not available"),
                int(creator.get("subscribers", 0)),
                int(creator.get("total_views", 0)),
                int(creator.get("total_videos", 0))
            ))

        connection.commit()

    finally:
        connection.close()


def get_all_creators():
    """Retrieve all saved creators."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM creators
            ORDER BY subscribers DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def save_search_history(keyword, results_count):
    """Store a creator search."""

    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO search_history (
                keyword,
                results_count
            )
            VALUES (?, ?)
        """, (keyword, results_count))

        connection.commit()

    finally:
        connection.close()


def save_recommendations(recommendations, brand_keyword):
    """Store recommendation rankings."""

def get_search_history():
    """Retrieve recent creator search history."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                keyword,
                results_count,
                searched_at
            FROM search_history
            ORDER BY searched_at DESC, id DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        for _, row in recommendations.iterrows():
            cursor.execute("""
                INSERT INTO recommendations (
                    channel_id,
                    brand_keyword,
                    suitability_score,
                    rank
                )
                VALUES (?, ?, ?, ?)
            """, (
                row["Channel ID"],
                brand_keyword,
                float(row["Suitability Score"]),
                int(row["Rank"])
            ))

        connection.commit()

    finally:
        connection.close()
