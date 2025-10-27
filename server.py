import os
import csv
from datetime import datetime
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

# ----------------------------
# Configuration
# ----------------------------
app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']  # Required for flash messages

# Load DB config from environment variables (set these in PythonAnywhere)
DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
}


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------
# Helper Functions
# ----------------------------
def get_db_connection():
    """Create a new database connection per request."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        logger.error(f"Database connection failed: {e}")
        raise

def validate_form_data(data):
    """Basic validation for contact form."""
    email = data.get('email', '').strip()
    subject = data.get('subject', '').strip()
    message = data.get('message', '').strip()

    if not email or not subject or not message:
        return False, "All fields are required."
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Please enter a valid email address."
    if len(message) > 1000:
        return False, "Message is too long (max 1000 characters)."
    if len(subject) > 100:
        return False, "Subject is too long (max 100 characters)."

    return True, {"email": email, "subject": subject, "message": message}

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def my_home():
    return render_template('index.html')

@app.route("/<path:page_name>")
def html_page(page_name):
    # Prevent directory traversal (e.g., ../../etc/passwd)
    if '..' in page_name or page_name.startswith('/'):
        return "Invalid page", 404
    return render_template(page_name)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Validate input
    is_valid, result = validate_form_data(request.form)
    if not is_valid:
        flash(result, 'error')
        return redirect('/contact.html')

    data = result

    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # ✅ REMOVED created_at — only insert email, subject, message
        insert_stmt = "INSERT INTO users (email, subject, message) VALUES (%s, %s, %s)"
        cursor.execute(insert_stmt, (data['email'], data['subject'], data['message']))
        connection.commit()

        flash("Thank you! Your message has been sent.", "success")
        return redirect('/thankyou.html')

    except Exception as e:
        logger.exception("Form submission failed")
        flash("Sorry, an error occurred. Please try again later.", "error")
        return redirect('/contact.html')
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# ----------------------------
# Error Handlers
# ----------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return "An internal error occurred.", 500
