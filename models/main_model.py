import threading
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from models.db_handler import DBHandler
from models.readme_driller import ReadmeDriller
import atexit
from models.git_traversal import GitTraversal


class MainModel:
    """
    Class that represents the main model of the project. Handles all database operations and writing to file.
    """
    def __init__(self):
        """
        Initializes the main model.
        """

        # Create the database.
        self.db_handler = DBHandler('repo_data.db')
        self.readme_driller = ReadmeDriller()

        # Register a cleanup of the database when program exits.
        atexit.register(self.cleanup)
        self.git_traversal = GitTraversal()

    def set_repo(self, repo_url, callback=None):
        """
        Sets the repo and inserts the data into the database.
        :param repo_url: URL of the repository.
        :param callback: Callback method.
        """
        self.git_traversal.set_repo(repo_url)

        self.readme_driller.clone_and_extract_readme(repo_url)


        def background_task():
            """
            Runs the background task of the insertion into the database.
            """
            try:
                result = self.db_handler.insert_data_into_db(repo_url)
                if result != "Success":
                    callback(None, "Was not able to get the repository, please try again, "
                                   "make sure to enter a valid Git repository URL.")
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

    def get_all_authors_and_their_commits(self):
        """
        Gets all authors and their commits.
        :return: Returns all authors and their commits.
        """
        return self.db_handler.get_all_authors_and_their_commits()

    def get_auths_commits_and_files(self):
        return self.db_handler.get_all_authors_commits_and_files()

    def get_top_10_files_per_user(self):
        """
        Gets top 10 files per user.
        :return: Dictionary with top 10 files.
        """
        data = self.db_handler.get_top_files_per_user()
        top_10_per_user = {}

        for name, file_path, changes in data:
            if name not in top_10_per_user:
                top_10_per_user[name] = {}

            # Only keep top 10 entries per user
            if len(top_10_per_user[name]) < 10:
                top_10_per_user[name][file_path] = changes

        return top_10_per_user

    def structure_monthly_activity_by_author(self):
        """
        Gets structured monthly activity data per author.
        :return: Dictionary with structured monthly data.
        """
        today = datetime.now()

        # Adjust strftime to generate month names without the year.
        readable_past_12_months = [(today - relativedelta(months=11 - i)).strftime("%b") for i in range(12)]

        # Get monthly commits.
        data = self.db_handler.get_monthly_commits_by_author()

        # Initialize the dictionary.
        structured_data = defaultdict(lambda: {month: 0 for month in readable_past_12_months})

        for month_year, name, commits_count in data:
            readable_month_year = datetime.strptime(month_year, "%Y-%m").strftime("%b")

            # Ensure we fill the commit counts for each author correctly.
            if readable_month_year in structured_data[name]:
                structured_data[name][readable_month_year] = commits_count

        return dict(structured_data)

    def get_timeline(self):
        """
        Gets timeline of activity.
        :return: Dictionary with monthly commit data.
        """
        data = self.db_handler.get_commit_counts_past_year()

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
        """
        Writes data to a file.
        :return: True if the writing to file was successful.
        """
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
            return True

    def cleanup(self):
        """
        Delete all data from the database and empty the file.
        """

        filename = "support//repo_stats.py"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("")
        if self.db_handler.database_has_values():
            self.db_handler.clear_database()
