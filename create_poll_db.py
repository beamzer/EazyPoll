import sqlite3
import configparser
from datetime import datetime
import uuid
import os

POLL_DB_FILE = 'poll_database.db'

def read_email_list(filename):
    try:
        with open(filename, 'r') as file:
            # Read lines and remove whitespace, empty lines
            emails = [line.strip() for line in file if line.strip()]
        return emails
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        exit(1)

def create_database():
    conn = sqlite3.connect(POLL_DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS polls
                 (token TEXT PRIMARY KEY,
                  email TEXT,
                  vote TEXT,
                  voted_at DATETIME)''')
    conn.commit()
    conn.close()

def read_config():
    config = configparser.ConfigParser()
    config_file = 'config.ini'
    
    if not os.path.exists(config_file):
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please ensure config.ini exists in the current directory.")
        exit(1)
    
    try:
        config.read(config_file)
    except Exception as e:
        print(f"Error reading configuration file '{config_file}': {str(e)}")
        exit(1)
    
    # Validate required sections and variables
    required_sections = ['files']
    required_vars = {
        'files': ['recipients_file']
    }
    
    for section in required_sections:
        if section not in config:
            print(f"Error: Missing required section '[{section}]' in {config_file}")
            exit(1)
            
        for var in required_vars[section]:
            if var not in config[section]:
                print(f"Error: Missing required variable '{var}' in section '[{section}]' of {config_file}")
                exit(1)
    
    return config

def check_existing_database():
    """Check if poll database file exists and handle accordingly"""
    if os.path.exists(POLL_DB_FILE):
        print(f"Warning: Database file '{poll_db_file}' already exists!")
        print("This will delete all existing poll data including any votes that may have been cast.")
        
        while True:
            response = input("Do you want to remove the existing database and create a new one? (y/n): ").lower().strip()
            
            if response in ['y', 'yes']:
                try:
                    os.remove(poll_db_file)
                    print(f"Existing database '{poll_db_file}' has been removed.")
                    return True
                except Exception as e:
                    print(f"Error removing database file: {str(e)}")
                    exit(1)
            elif response in ['n', 'no']:
                print("Operation aborted. Existing database preserved.")
                exit(0)
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    return True

def initialize_database():
    # Read configuration (this will check for config.ini first)
    config = read_config()
    
    # Check for existing database and handle accordingly
    check_existing_database()
    
    # Get email file path from config
    email_file = config['files']['recipients_file']

    # Read email addresses from file
    print(f"Reading email addresses from {email_file}...")
    email_list = read_email_list(email_file)

    # Create database if it doesn't exist
    create_database()
    
    # Initialize database with email addresses
    conn = sqlite3.connect(POLL_DB_FILE)
    c = conn.cursor()

    try:
        for email in email_list:
            token = str(uuid.uuid4())
            c.execute("INSERT INTO polls (email, token) VALUES (?, ?)",
                     (email, token))
        conn.commit()
        print(f"Successfully initialized database with {len(email_list)} email addresses")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
