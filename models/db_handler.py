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

        # Create a table for the commits, containing an ID, contributor ID, the message
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS commits (
                        id INTEGER PRIMARY KEY,
                        author_id INTEGER,
                        message TEXT,
                        FOREIGN KEY (author_id) REFERENCES authors (id)
                    );
                ''')

        # Create a table for the files that were modified.
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS commit_files (
                           id INTEGER PRIMARY KEY,
                           commit_id INTEGER,
                           file_path TEXT,
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

                cursor.execute('INSERT INTO commits (author_id, message) VALUES (?, ?)',
                               (author_id, commit.msg))
                commit_id = cursor.lastrowid

                # For each modified file in the commit, add the modified files.
                for mod in commit.modified_files:
                    cursor.execute('INSERT INTO commit_files (commit_id, file_path) VALUES (?, ?)',
                                   (commit_id, mod.new_path))

                conn.commit()
        except Exception as e:
            error_message = "Please try again with an existing repository."
        else:
            return "Success"
        finally:
            if 'conn' in locals():
                conn.close()
        return error_message

    def get_all_authors_commits_and_files(self):
        """
        Retrieves all authors along with their commits and the filenames of changed files for each commit.
        :return: Dictionary with author as key, and each value being a list of tuples (commit message, list of filenames).
        """
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Execute SQL query to retrieve author details, their commits, and associated file changes
        cursor.execute('''
                SELECT a.name, c.message, GROUP_CONCAT(cf.file_path) as files
                FROM authors a
                JOIN commits c ON a.id = c.author_id
                LEFT JOIN commit_files cf ON c.id = cf.commit_id
                GROUP BY c.id
                ORDER BY a.name;
            ''')

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Organize the results into a structured format
        # Here we create a dictionary where each key is an author's name,
        # and the value is a list of tuples (commit message, [list of filenames]).
        authors_commits_files = {}
        for name, message, files in results:
            if name not in authors_commits_files:
                authors_commits_files[name] = []
            # Split the concatenated filenames back into a list
            file_list = files.split(',') if files else []
            authors_commits_files[name].append((message, file_list))

        return authors_commits_files

    def get_all_authors_and_their_commits(self):
        """
        Retrieves all authors along with their commits and the file paths of the changed files from the database.
        :return: Dictionary with author as key, and each value being a list of tuples (commit message, list of file paths).
        """
        # Connect to the database
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Execute SQL query to retrieve author details, their commits, and associated file changes
        cursor.execute('''
                SELECT a.name, c.message, GROUP_CONCAT(cf.file_path) AS files
                FROM authors a
                JOIN commits c ON a.id = c.author_id
                LEFT JOIN commit_files cf ON c.id = cf.commit_id
                GROUP BY c.id
                ORDER BY a.name;
            ''')

        # Fetch the results
        results = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Organize the results into a structured format
        # Here we create a dictionary where each key is an author's name,
        # and the value is a list of tuples (commit message, [list of file paths]).
        authors_commits_files = {}
        for name, message, files in results:
            if name not in authors_commits_files:
                authors_commits_files[name] = []
            # Split the concatenated file paths back into a list
            file_list = files.split(',') if files else []
            authors_commits_files[name].append((message, file_list))

        return authors_commits_files

    def get_commit_counts_by_author(self):
        """
        Retrieves the number of commits made by each author.
        :return: A dictionary with author names as keys and commit counts as values.
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT a.name, COUNT(c.id)
            FROM authors a
            JOIN commits c ON a.id = c.author_id
            GROUP BY a.name;
        ''')

        results = cursor.fetchall()
        conn.close()

        # Organize results into a dictionary
        commit_counts = {name: count for name, count in results}
        return commit_counts

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
