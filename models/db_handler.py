import sqlite3

from dateutil.relativedelta import relativedelta
from pydriller import Repository
import calendar
from datetime import datetime, timedelta

class DBHandler:
    # TODO fixa så att det skrivs i filer engligt dummy fil
    # TODO fixa 5 top filer med antal commits
    # TODO fixa varje authors top 5 med antal commits

    def __init__(self, db_name):
        self.db_name = db_name
        self.create_database()

    """Creates the database with author, commit, and commit-files tables."""
    def create_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create a table for the contributors, containing an ID, name, and email.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE
            );
        ''')

        # Create a table for the commits, containing an ID, contributor ID, and the message.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commits (
                id INTEGER PRIMARY KEY,
                author_id INTEGER,
                message TEXT,
                date DATE,
                FOREIGN KEY (author_id) REFERENCES authors (id)
            );
        ''')

        # Create a table for the files and filepaths that were modified.
        cursor.execute('''
                CREATE TABLE IF NOT EXISTS commit_files (
                    id INTEGER PRIMARY KEY,
                    commit_id INTEGER,
                    file_name TEXT,
                    file_path TEXT,
                    FOREIGN KEY (commit_id) REFERENCES commits (id)
                );
            ''')

        conn.commit()
        conn.close()

    """Inserts the data from the repo into the db."""
    def insert_data_into_db(self, repo_url):
        # TODO ta bort github users + lower case undvik duplicates, måste vara unik
        self.create_database()  # Ensure the database and tables exist
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # For each commit, insert the author and commit info into the tables.
            for commit in Repository(repo_url).traverse_commits():
                # Insert author if not exists
                cursor.execute('INSERT OR IGNORE INTO authors (name, email) VALUES (?, ?)',
                               (commit.author.name, commit.author.email))
                cursor.execute('SELECT id FROM authors WHERE email = ?', (commit.author.email,))
                author_id = cursor.fetchone()[0]


                # Format the date and insert commit
                #formatted_date = commit.author_date.strftime("%Y-%m-%d %H:%M:%S")
                formatted_date = commit.committer_date.strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute('INSERT INTO commits (author_id, message, date) VALUES (?, ?, ?)',
                               (author_id, commit.msg, formatted_date))
                commit_id = cursor.lastrowid

                # For each modified file in the commit, add the modified files and their filepaths.
                for mod in commit.modified_files:
                    cursor.execute('INSERT INTO commit_files (commit_id, file_name, file_path) VALUES (?, ?, ?)',
                                   (commit_id, mod.filename, mod.new_path))

                conn.commit()
        except Exception as e:
            error_message = "Please try again with an existing repository."
        else:
            return "Success"
        finally:
            if 'conn' in locals():
                conn.close()
        return error_message

    def get_authors_with_amount_of_commits(self):
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # SQL query to count commits per author
        cursor.execute('''
                SELECT a.name, COUNT(c.id) AS total_commits
                FROM authors a
                JOIN commits c ON a.id = c.author_id
                GROUP BY a.id
            ''')

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Convert the results into a dictionary
        total_commits_by_contributor = {name: total_commits for name, total_commits in results}
        return total_commits_by_contributor

    def get_top_5_changed_files(self):
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # SQL query to find the top 5 file names by occurrence
        cursor.execute('''
               SELECT file_name, COUNT(file_name) AS occurrence
               FROM commit_files
               GROUP BY file_name
               ORDER BY occurrence DESC
               LIMIT 5
           ''')

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Convert the results into a dictionary
        top_5_changed_files = {file_name: occurrence for file_name, occurrence in results}
        return top_5_changed_files

    def get_top_files_per_user(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Fetches the number of times each file has been modified by each author
        cursor.execute('''
            SELECT a.name, cf.file_name, COUNT(cf.file_name) as changes
            FROM commit_files cf
            JOIN commits c ON cf.commit_id = c.id
            JOIN authors a ON c.author_id = a.id
            GROUP BY a.id, cf.file_name
            ORDER BY a.name, changes DESC
        ''')

        results = cursor.fetchall()
        conn.close()
        return results

    def get_monthly_commits_by_author(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Get today's date and the date 12 months ago
        today = datetime.now()
        twelve_months_ago = today - relativedelta(months=12)

        cursor.execute('''
                SELECT 
                    strftime('%Y-%m', date) AS month_year, 
                    a.name, 
                    COUNT(*) AS commits_count
                FROM 
                    commits c
                    JOIN authors a ON c.author_id = a.id
                WHERE 
                    c.date >= ?
                GROUP BY 
                    month_year, a.name
                ORDER BY 
                    month_year ASC
            ''', (twelve_months_ago.strftime('%Y-%m-%d'),))

        results = cursor.fetchall()
        conn.close()
        return results

    """Gets the total amount of commits."""
    def get_total_commits(self):
        # Connect to DB
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM commits')
        total_commits = cursor.fetchone()[0]  # Count the rows

        conn.close()
        return total_commits

    def get_all_commits(self):
        # Connect to DB
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT message FROM commits')
        # Fetch all results and transform each tuple to its first element
        commits = [commit[0] for commit in cursor.fetchall()]

        conn.close()
        return commits

    """Gets the names of all contributors."""
    def get_all_contributors(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Select only the name column from the authors table
        cursor.execute('SELECT name FROM authors')

        # Fetch all results and extract names from tuples
        contributors = [row[0] for row in cursor.fetchall()]

        conn.close()

        return contributors

    """Gets the most active month."""
    def get_most_active_month(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Get date 12 months ago
        twelve_months_ago = datetime.now() - timedelta(days=365)
        formatted_date = twelve_months_ago.strftime("%Y-%m-%d")

        cursor.execute('''
                    SELECT strftime("%m", date) as month, strftime("%Y", date) as year, COUNT(*)
                    FROM commits
                    WHERE date >= ?
                    GROUP BY year, month
                ''', (formatted_date,))
        monthly_commit_counts = cursor.fetchall()
        conn.close()

        if not monthly_commit_counts:
            return None

        # Convert month number to month name
        most_active_month = max(monthly_commit_counts, key=lambda x: x[2])

        # Find the month with the highest commit count
        month_name = calendar.month_name[int(most_active_month[0])]
        return f"{month_name}"

    """Gets the amount of commits each month for the past 12 months."""
    def get_commit_counts_past_year(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Prepare the list for the last 12 months
        last_12_months = [(datetime.now() - timedelta(days=30 * i)).strftime("%Y-%m") for i in range(11, -1, -1)]

        # Initialize commit counts for each month with 0
        commit_counts = dict.fromkeys(last_12_months, 0)

        # Query to get commit counts for available months in the last year
        cursor.execute('''
            SELECT strftime("%Y-%m", date) AS month, COUNT(*) 
            FROM commits 
            WHERE date >= ?
            GROUP BY month
        ''', (last_12_months[0],))

        # Fetch the results once and store them
        total_commits = cursor.fetchall()

        # Use the stored results
        for month, count in total_commits:
            if month in commit_counts:
                commit_counts[month] = count

        conn.close()

        # Return commit counts as a list
        return [commit_counts[month] for month in last_12_months]

    """Gets all commit info (message, date, author email, filenames and filepath for a contributor."""
    def get_commit_data_with_files_for_author(self, author_email):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Retrieve commits and file changes for a specific author
        cursor.execute('''
            SELECT c.id, c.message, c.date, a.name, a.email, f.file_name, f.file_path 
            FROM commits c
            JOIN authors a ON c.author_id = a.id
            LEFT JOIN commit_files f ON c.id = f.commit_id
            WHERE a.email = ?
            ORDER BY c.date
        ''', (author_email,))
        rows = cursor.fetchall()

        conn.close()

        # Process rows. TODO other values to return
        commit_data = {}
        for row in rows:
            commit_id, message, date, author_name, author_email, file_name, file_path = row
            if commit_id not in commit_data:
                commit_data[commit_id] = {
                    "message": message,
                    "date": date,
                    "author": {"name": author_name, "email": author_email},
                    "files": []
                }
            if file_name:  # Check if file_name is not None
                commit_data[commit_id]["files"].append({"file_name": file_name, "file_path": file_path})

        return commit_data

    def database_has_values(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM commits')
        commit_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM authors')
        author_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM commit_files')
        commit_files = cursor.fetchone()[0]

        conn.close()
        return commit_count > 0 or author_count > 0 or commit_files > 0

    def clear_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM commits')
            cursor.execute('DELETE FROM authors')
            cursor.execute('DELETE FROM commit_files')

            conn.commit()
            conn.close()
            print("Database successfully cleared.")
        except Exception as e:
            print(f"Error clearing database: {e}")

