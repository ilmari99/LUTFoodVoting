import sqlite3
from datetime import datetime

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('user_database.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# SQL query to create the users table
create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''
# Execute the query to create the table
cursor.execute(create_table_query)

# Function to add a new user
def add_user(username, email, password):
    insert_query = 'INSERT INTO users (username, email, password) VALUES (?, ?, ?);'
    cursor.execute(insert_query, (username, email, password))
    conn.commit()  # Save the changes to the database
    print(f'User {username} added successfully!')

# Example of adding a new user
add_user('john_doe', 'john@example.com', 'securepassword123')

# Close the database connection when done
conn.close()
