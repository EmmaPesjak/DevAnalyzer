import sqlite3

from dateutil.relativedelta import relativedelta
from pydriller import Repository
from datetime import datetime

class DBHandler:
    """
    Class to handle the repository data, creating and connecting to the database.
    """

    def __init__(self, db_name):
        """
        Initialize the DBHandler class.
        :param db_name: Name of database.
        """
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """
        Creates the database with author, commit, and commit-files tables.
        """
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

        # Create a table for the commits, containing an ID, contributor ID, the message, and the date.
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS commits (
                        id INTEGER PRIMARY KEY,
                        author_id INTEGER,
                        message TEXT,
                        date DATE,
                        FOREIGN KEY (author_id) REFERENCES authors (id)
                    );
                ''')

        # Create a table for the files that were modified.
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS commit_files (
                           id INTEGER PRIMARY KEY,
                           commit_id INTEGER,
                           file_name TEXT,
                           FOREIGN KEY (commit_id) REFERENCES commits (id)
                       );
                   ''')

        conn.commit()
        conn.close()

    def insert_data_into_db(self, repo_url):
        """
        Inserts the repository data into database.
        :param repo_url: Url of the repository.
        :return: If the insertion was successful or not.
        """
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
                formatted_date = commit.author_date.strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute('INSERT INTO commits (author_id, message, date) VALUES (?, ?, ?)',
                               (author_id, commit.msg, formatted_date))
                commit_id = cursor.lastrowid

                # For each modified file in the commit, add the modified files.
                for mod in commit.modified_files:
                    cursor.execute('INSERT INTO commit_files (commit_id, file_name) VALUES (?, ?)',
                                   (commit_id, mod.filename))

                conn.commit()
        except Exception as e:
            error_message = "Please try again with an existing repository."
        else:
            return "Success"
        finally:
            if 'conn' in locals():
                conn.close()
        return error_message

    def get_all_authors_and_their_commits(self):
        """
        Retrieves all authors along with their commits from the database.
        :return: Dictionary with author and their commits.
        """
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Execute SQL query to retrieve author details and their commits
        cursor.execute('''
                SELECT a.name, c.message
                FROM authors a
                JOIN commits c ON a.id = c.author_id
                ORDER BY a.name;
            ''')

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Organize the results into a structured format
        # Here we create a dictionary where each key is an author's name,
        # and the value is a list of commit messages.
        authors_commits = {}
        for name, message in results:
            if name not in authors_commits:
                authors_commits[name] = []
            authors_commits[name].append(message)

        return authors_commits

    def get_top_10_changed_files(self):
        """
        Retrieves the top 10 changed files.
        :return: Dictionary with filenames and amount of times they have been changed.
        """
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # SQL query to find the top 10 file names by occurrence
        cursor.execute('''
               SELECT file_name, COUNT(file_name) AS occurrence
               FROM commit_files
               GROUP BY file_name
               ORDER BY occurrence DESC
               LIMIT 10
           ''')

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Convert the results into a dictionary
        top_10_changed_files = {file_name: occurrence for file_name, occurrence in results}
        return top_10_changed_files

    def get_top_files_per_user(self):
        """
        Retrieves the top 10 files per user.
        :return: Top 10 files per user.
        """
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
        """
        Retrieves the monthly commits by author for the past 12 months.
        :return: Months with amount of commits per author.
        """
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

    def get_commit_counts_past_year(self):
        """
        Retrieves a timeline of amount of commits the past 12 months.
        :return: Result of retrieval.
        """

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Get today's date and the date 12 months ago
        today = datetime.now()
        twelve_months_ago = today - relativedelta(months=12)

        cursor.execute('''
                SELECT
                    strftime('%Y-%m', date) AS month_year,
                    COUNT(*) AS commits_count
                FROM
                    commits
                WHERE
                    date >= ?
                GROUP BY
                    month_year
                ORDER BY
                    month_year ASC
            ''', (twelve_months_ago.strftime('%Y-%m-%d'),))

        results = cursor.fetchall()
        conn.close()
        return results

    def database_has_values(self):
        """
        Checks if the database has values.
        :return: True or false based on result.
        """
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
        """
        Clears the database.
        """
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
