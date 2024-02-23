
import sqlite3
from pydriller import Repository
import calendar

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

    def get_all_contributors(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM authors')

        contributors = cursor.fetchall()

        conn.commit()
        conn.close()

        return contributors

    def get_most_active_month(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Query to get month number and year, along with commit count
        cursor.execute('SELECT strftime("%m", date) as month, strftime("%Y", date) as year, COUNT(*) FROM commits GROUP BY year, month')
        monthly_commit_counts = cursor.fetchall()

        conn.close()

        if not monthly_commit_counts:
            return None

        # Find the month with the highest commit count
        most_active_month = max(monthly_commit_counts, key=lambda x: x[2])

        # Convert month number to month name
        month_name = calendar.month_name[int(most_active_month[0])]
        return f"{month_name} {most_active_month[1]} with {most_active_month[2]} commits."


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

