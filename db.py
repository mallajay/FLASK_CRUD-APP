import os
import sqlite3
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the directory where db.py is located
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the database directory and ensure it exists
_database_directory = os.path.join(_BASE_DIR, "database")
os.makedirs(_database_directory, exist_ok=True)

# Define the full path to the SQLite database file
_database_path = os.path.join(_database_directory, "CRUD.db")


def get_db_connection():
    """Connect to the SQLite database."""
    try:
        logger.debug(f"Connecting to database at {_database_path}")
        connection = sqlite3.connect(_database_path)
        connection.row_factory = sqlite3.Row  # Enables name-based access to columns
        return connection
    except sqlite3.Error as e:
        logger.error(f"Error connecting to the database: {e}")
        raise


def get_total_changes():
    """Get the total number of changes in the database."""
    try:
        connection = get_db_connection()
        total_changes = connection.total_changes
        return total_changes
    except sqlite3.Error as e:
        logger.error(f"Error retrieving total changes: {e}")
        raise
    finally:
        if connection:
            connection.close()


def initialize_database():
    """Initialize the database with necessary tables."""
    try:
        logger.debug("Initializing database...")
        connection = get_db_connection()
        cursor = connection.cursor()
        # Example table creation
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )
        # Add other table creations as needed
        connection.commit()
        logger.debug("Database initialized.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing the database: {e}")
        raise
    finally:
        if connection:
            connection.close()


def create_user(name, email):
    """Create a new user in the database."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (name, email) VALUES (?, ?)
            """,
            (name, email),
        )
        connection.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"Integrity error: {e}")
        raise  # Reraise to be handled by the calling code
    except sqlite3.Error as e:
        logger.error(f"Error creating user: {e}")
        raise
    finally:
        if connection:
            connection.close()


def get_user(user_id):
    """Get a user by ID."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT * FROM users WHERE id = ?
            """,
            (user_id,),
        )
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        logger.error(f"Error retrieving user with ID {user_id}: {e}")
        raise
    finally:
        if connection:
            connection.close()


def get_all_users():
    """Get all users."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT * FROM users
            """
        )
        users = cursor.fetchall()
        return users
    except sqlite3.Error as e:
        logger.error(f"Error retrieving all users: {e}")
        raise
    finally:
        if connection:
            connection.close()


def update_user(user_id, name, email):
    """Update user details."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE users SET name = ?, email = ? WHERE id = ?
            """,
            (name, email, user_id),
        )
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating user with ID {user_id}: {e}")
        raise
    finally:
        if connection:
            connection.close()


def delete_user(user_id):
    """Delete a user."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            DELETE FROM users WHERE id = ?
            """,
            (user_id,),
        )
        connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        raise
    finally:
        if connection:
            connection.close()
