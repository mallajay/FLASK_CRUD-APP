import os
from flask import Flask, request, jsonify
import db
import sqlite3

app = Flask(__name__)


def initialize_db():
    try:
        db.initialize_database()
    except Exception as e:
        app.logger.error(f"Error initializing database: {e}")
        raise


@app.route("/users", methods=["POST"])
def create_user():
    """Create a new user."""
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        # Try to create the user in the database
        db.create_user(name, email)
        return jsonify({"message": "User created successfully"}), 201

    except sqlite3.IntegrityError:
        # Handle unique constraint error (e.g., duplicate email)
        return jsonify({"error": "User with this email already exists"}), 400
    except Exception as e:
        # Handle any other exceptions
        app.logger.error(f"Error creating user: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get user by ID."""
    try:
        user = db.get_user(user_id)
        if user:
            return jsonify(dict(user)), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        app.logger.error(f"Error retrieving user with ID {user_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/users", methods=["GET"])
def get_all_users():
    """Get all users."""
    try:
        users = db.get_all_users()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        app.logger.error(f"Error retrieving all users: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update user details."""
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

        db.update_user(user_id, name, email)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error updating user with ID {user_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user."""
    try:
        db.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error deleting user with ID {user_id}: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def hello_world():
    """Basic route."""
    SECRET_KEY = os.getenv("MY_SECRET")
    print("SECRET_KEY:", SECRET_KEY)
    return "<p>Hello, World!</p>"


@app.route("/total_changes")
def show_total_changes():
    """Show total changes in the database."""
    try:
        total_changes = db.get_total_changes()
        return f"Total changes in the database: {total_changes}"
    except Exception as e:
        app.logger.error(f"Error retrieving total changes: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
