import threading
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from models.db_handler import DBHandler
import atexit
from models.git_traversal import GitTraversal
from collections import OrderedDict


class MainModel:

    def __init__(self):
        self.db_handler = DBHandler('repo_data.db')
        atexit.register(self.cleanup)
        self.git_traversal = GitTraversal()

    def set_repo(self, repo_url, callback=None):
        """Inserts the repository into DB."""
        self.git_traversal.set_repo(repo_url)

        def background_task():
            try:
                # Assuming this function returns some result or raises an exception upon failure
                result = self.db_handler.insert_data_into_db(repo_url)
                if result != "Success":
                    callback(None, "Error!")
                elif callback:
                    # Use callback to send success data back
                    callback(result, None)
            except Exception as e:
                if callback:
                    # Use callback to send the exception back
                    callback(None, e)

        # Start the background task
        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()

    def get_top_10_files_per_user(self):
        data = self.db_handler.get_top_files_per_user()
        top_10_per_user = {}

        for name, file_name, changes in data:
            if name not in top_10_per_user:
                top_10_per_user[name] = {}

            # Only keep top 10 entries per user
            if len(top_10_per_user[name]) < 10:
                top_10_per_user[name][file_name] = changes

        return top_10_per_user

    def structure_monthly_activity_by_author(self):
        today = datetime.now()

        # Adjust strftime to generate month names without the year.
        readable_past_12_months = [(today - relativedelta(months=11 - i)).strftime("%b") for i in range(12)]

        data = self.db_handler.get_monthly_commits_by_author()

        structured_data = defaultdict(lambda: {month: 0 for month in readable_past_12_months})

        for month_year, name, commits_count in data:
            readable_month_year = datetime.strptime(month_year, "%Y-%m").strftime("%b")  # Adjusted to match format.

            # Ensure we fill the commit counts for each author correctly.
            if readable_month_year in structured_data[name]:
                structured_data[name][readable_month_year] = commits_count

        return dict(structured_data)

    def get_timeline(self):
        data = self.db_handler.get_commit_counts_past_year()
        #TODO: OBS radera inte koden som är bortkommenterad här under, den är till för om man vill köra git_traversal

        # Ensure month names are in descending order (most recent first)
        # # Sort data keys to ensure month names are in ascending order (oldest first)
        # data_keys_sorted = sorted(data.keys(), reverse=False)
        #
        # readable_format_data = {}
        # for month_year in data_keys_sorted:
        #     month_name = datetime.strptime(month_year, "%Y-%m").strftime("%b")
        #     readable_format_data[month_name] = data[month_year]
        #
        # return readable_format_data
        today = datetime.now()
        # Initialize a dictionary for the past 12 months
        structured_data = {((today - relativedelta(months=i)).strftime("%Y-%m")): 0 for i in range(12)}

        # Fill in the data from the list of tuples
        for month_year, commits_count in data:
            if month_year in structured_data:
                structured_data[month_year] = commits_count

        # Convert 'month_year' to month names without year
        readable_format_data = {}
        for month_year in reversed(list(structured_data.keys())):
            month_name = datetime.strptime(month_year, "%Y-%m").strftime("%b")
            readable_format_data[month_name] = structured_data[month_year]

        return readable_format_data

    def write_to_file(self):
        start_time = time.time()
        filename = "support//repo_stats.py"

        total_commits_by_contributor = self.git_traversal.get_authors_with_amount_of_commits()
        top_10_changed_files = self.db_handler.get_top_10_changed_files()
        top_10_per_user = self.get_top_10_files_per_user()
        monthly_commits_by_users = self.structure_monthly_activity_by_author()
        total_monthly_commits = self.get_timeline()

        # Prepare the content to be written as valid Python code
        content_to_write = (
            f"total_commits_by_contributor = {total_commits_by_contributor}\n"
            f"top_10_changed_files = {top_10_changed_files}\n"
            f"top_10_per_user = {top_10_per_user}\n"
            f"monthly_commits_by_contributor = {monthly_commits_by_users}\n"
            f"total_monthly_commits = {total_monthly_commits}\n"
        )

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content_to_write)
            print("Saved")
            end_time = time.time()
            print(f"Writing to file took {end_time - start_time:.2f} seconds.")
            return True


    # TODO BUG; DB doesn't always clear up after exit.
    """ Empties the database on exit."""
    def cleanup(self):

        filename = "support//repo_stats.py"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("")
        if self.db_handler.database_has_values():
            self.db_handler.clear_database()
        print("Database cleared.")
