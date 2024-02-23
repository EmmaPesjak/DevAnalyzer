from pydriller import Repository
import json
from collections import defaultdict

from models.db_handler import DBHandler
import atexit

class MainModel:

    def __init__(self):
        self.db_handler = DBHandler('repo_data.db')
        atexit.register(self.cleanup)
        #self.author_commits = defaultdict(list)

    """Sets the repo url."""
    def set_repo(self, repo_url):
        self.db_handler.insert_data_into_db(repo_url)

    def get_total_amount_of_commits(self):
        return self.db_handler.get_total_commits()

    def get_all_contributors(self):
        return self.db_handler.get_all_contributors()

    def get_most_active_month(self):
        return self.db_handler.get_most_active_month()

    """Empties the database on exit."""
    def cleanup(self):
        self.db_handler.clear_database()
        print("Database cleared.")

    """Retrieves the repo data and adds it to the set."""
    # def process_commits(self):
    #     for commit in self.repo.traverse_commits():
    #         author = commit.author.name
    #         if author not in self.author_commits:
    #             self.author_commits[author] = []
    #
    #         commit_info = {
    #             "message": commit.msg,
    #             "date": commit.author_date.strftime("%Y-%m-%d %H:%M:%S"),
    #             "files": [{"file_name": mod.filename, "file_path": mod.new_path} for mod in commit.modified_files]
    #         }
    #
    #         self.author_commits[author].append(commit_info)
    #         #self.author_commits[author].append(commit.msg)

