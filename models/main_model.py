from pydriller import Repository
import json
from collections import defaultdict

from models.db_handler import DBHandler
import atexit


# TODO
# get info from repo;
# contributors with all its commits
# 1. store it in a file with; author: commits[]
# 2. to get author names, loop through the keys of the dictionary
# 3. to get total amount of commits, count the size of each list mapped to the author
# 4. to get author with amount of commits, get author key and size of commit list
# 5. later; NLP categorize


class MainModel:

    def __init__(self):
        self.db_handler = DBHandler('repo_data.db')
        atexit.register(self.cleanup)
        #self.author_commits = defaultdict(list)

    """Sets the repo url."""
    def set_repo(self, repo_url):
        self.db_handler.insert_data_into_db(repo_url)

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

