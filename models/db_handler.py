from pydriller import Repository
import sqlite3

import sqlite3
from pydriller import Repository

class DBHandler:

    def __init__(self, db_name):
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commits (
                id INTEGER PRIMARY KEY,
                author_id INTEGER,
                message TEXT,
                date DATE,
                FOREIGN KEY (author_id) REFERENCES authors (id)
            );
        ''')

        conn.commit()
        conn.close()

    def insert_data_into_db(self, repo_url):
        self.create_database()  # Ensure the database and tables exist
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        for commit in Repository(repo_url).traverse_commits():
            # Insert author if not exists
            cursor.execute('INSERT OR IGNORE INTO authors (name, email) VALUES (?, ?)',
                           (commit.author.name, commit.author.email))
            cursor.execute('SELECT id FROM authors WHERE email = ?', (commit.author.email,))
            author_id = cursor.fetchone()[0]

            # Format the date and insert commit
            formatted_date = commit.author_date.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('INSERT INTO commits (author_id, message, date) VALUES (?, ?, ?)',
                           (author_id, commit.msg, formatted_date))

        conn.commit()
        conn.close()

    """Gets the total amount of commits."""
    def get_total_commits(self):
        # Connect to DB
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM commits')
        total_commits = cursor.fetchone()[0]  # Count the rows

        conn.close()
        return total_commits

    def clear_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM commits')
            cursor.execute('DELETE FROM authors')

            conn.commit()
            conn.close()
            print("Database successfully cleared.")
        except Exception as e:
            print(f"Error clearing database: {e}")

