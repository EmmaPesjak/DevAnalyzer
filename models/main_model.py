import threading
from models.bert_analyzer import BertAnalyzer
from models.db_handler import DBHandler
from models.bert_readme_model import BertReadmeModel
import atexit


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
        self.readme_bert = BertReadmeModel()
        self.bert_analyzer = BertAnalyzer()

        # Register a cleanup of the database when program exits.
        atexit.register(self.cleanup)

    def set_repo(self, repo_url, callback=None):
        """
        Sets the repo and inserts the data into the database.
        :param repo_url: URL of the repository.
        :param callback: Callback method.
        """
        def background_task():
            """
            Runs the background task of the insertion into the database.
            """
            try:
                result = self.db_handler.insert_data_into_db(repo_url)
                if result != "Success":
                    callback(None, result)
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

    def analyze_commits(self):
        """
        Analyzes commit
        """
        all_commits = self.db_handler.get_all_authors_and_their_commits()
        self.bert_analyzer.analyze_commits(all_commits)

    def write_to_file(self):
        """
        Writes data to a file.
        :return: True if the writing to file was successful.
        """
        filename = "support//repo_stats.py"
        self.analyze_commits()

        # Retrieve information from database and BertAnalyzer.
        total_commits_by_contributor = self.db_handler.get_commit_counts_by_author()
        readme_summary = self.readme_bert.get_readme_summary()
        total_what_per_user = self.bert_analyzer.get_total_what_per_user()
        total_where_per_user = self.bert_analyzer.get_total_where_per_user()
        total_what = self.bert_analyzer.get_total_what()
        total_where = self.bert_analyzer.get_total_where()
        personal_summaries = self.bert_analyzer.get_personal_summary()
        overall_summary = self.bert_analyzer.get_overall_summary()

        # Prepare the content to be written
        content_to_write = (
            f"total_commits_by_contributor = {total_commits_by_contributor}\n"
            f'readme_summary = """{readme_summary}"""\n'
            f"total_what = {total_what}\n"
            f"total_where = {total_where}\n"
            f"total_what_per_user = {total_what_per_user}\n"
            f"total_where_per_user = {total_where_per_user}\n"
            f"personal_summaries = {personal_summaries}\n"
            f"overall_summary = \'{overall_summary}\'\n"
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
        filename = "support//Downloaded_README.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("")
        if self.db_handler.database_has_values():
            self.db_handler.clear_database()
