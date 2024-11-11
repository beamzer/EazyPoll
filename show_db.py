import sqlite3

def show_database_contents(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        print(f"\nContents of table '{table_name[0]}':")
        cursor.execute(f"SELECT * FROM {table_name[0]}")
        rows = cursor.fetchall()

        # Print column names
        column_names = [description[0] for description in cursor.description]
        print(column_names)

        # Print each row
        for row in rows:
            print(row)

    # Close the connection
    conn.close()

# Replace 'your_database.db' with the path to your SQLite database
show_database_contents('poll_database.db')