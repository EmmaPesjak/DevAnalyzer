from pydriller import Repository
import json
from collections import defaultdict

from models.db_handler import DBHandler
import atexit

class MainModel:

    def __init__(self):
        self.db_handler = DBHandler('repo_data.db')
        atexit.register(self.cleanup)

    """Inserts the repository into DB."""
    def set_repo(self, repo_url):
        self.db_handler.insert_data_into_db(repo_url)

    def get_total_amount_of_commits(self):
        return self.db_handler.get_total_commits()

    def get_all_contributors(self):
        return self.db_handler.get_all_contributors()

    def get_most_active_month(self):
        return self.db_handler.get_most_active_month()

    def get_all_months_activity(self):
        return self.db_handler.get_commit_counts_past_year()

    # TODO get the commit messages for user to process.
    def get_commit_data_with_files_for_author(self, author_email):
        return self.db_handler.get_commit_data_with_files_for_author(author_email)

    # TODO BUG; DB doesn't always clear up after exit.
    """ Empties the database on exit."""
    def cleanup(self):
        if self.db_handler.database_has_values():
            self.db_handler.clear_database()
        print("Database cleared.")
