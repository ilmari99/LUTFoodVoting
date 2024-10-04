import sqlite3

def fetch_all_data(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

        # Fetch all data from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        # Print column names
        print(" | ".join(columns))

        # Print rows
        for row in rows:
            print(" | ".join(map(str, row)))
        print("\n")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    fetch_all_data('C:\\Users\\ilmari\\Desktop\\Python\\LUTFoodVoting\\lunch_voting\\db.sqlite3')