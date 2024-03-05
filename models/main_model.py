import threading

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
    def set_repo(self, repo_url, callback=None):
        def background_task():
            try:
                # Assuming this function returns some result or raises an exception upon failure
                result = self.db_handler.insert_data_into_db(repo_url)
                if callback:
                    # Use callback to send success data back
                    callback(result, None)
            except Exception as e:
                if callback:
                    # Use callback to send the exception back
                    callback(None, e)

        # Start the background task
        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()

    def get_authors_with_amount_of_commits(self):
        return self.db_handler.get_authors_with_amount_of_commits()

    def get_total_amount_of_commits(self):
        return self.db_handler.get_total_commits()

    def get_all_commits(self):
        return self.db_handler.get_all_commits()

    def get_all_contributors(self):
        return self.db_handler.get_all_contributors()

    def get_most_active_month(self):
        return self.db_handler.get_most_active_month()

    def get_all_months_activity(self):
        return self.db_handler.get_commit_counts_past_year()

    # TODO get the commit messages for user to process.
    def get_commit_data_with_files_for_author(self, author_email):
        return self.db_handler.get_commit_data_with_files_for_author(author_email)

    def write_to_file(self):
        filename = "support//repo_stats.py"

        total_commits_by_contributor = self.db_handler.get_authors_with_amount_of_commits()
        top_5_changed_files = self.db_handler.get_top_5_changed_files()

        # Prepare the content to be written as valid Python code
        content_to_write = (
            f"total_commits_by_contributor = {total_commits_by_contributor}\n"
            f"top_5_changed_files = {top_5_changed_files}\n"
        )

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content_to_write)
            print("Saved")
            return True


    # TODO BUG; DB doesn't always clear up after exit.
    """ Empties the database on exit."""
    def cleanup(self):
        if self.db_handler.database_has_values():
            self.db_handler.clear_database()
        print("Database cleared.")
