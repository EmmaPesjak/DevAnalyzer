from pydriller import Repository
from pydriller.metrics.process.commits_count import CommitsCount
import json
from collections import defaultdict
from pydriller.metrics.process.contributors_count import ContributorsCount



# TODO
# get info from repo;
# contributors with all its commits
# 1. store it in a file with; author: commits[]
# 2. to get author names, loop through the keys of the dictionary
# 3. to get total amount of commits, count the size of each list mapped to the author
# 4. to get author with amount of commits, get author key and size of commit list
# 5. later; NLP categorize


class MainModel:

    """TODO
    Allt ska samlas i en fil
    Dra ner author med commit msg, datum, samt filnamn & filepath relaterat till committen

    """

    def __init__(self):
        self.repo = None
        #self.author_commits = {}  # Store authors and their commits
        self.author_commits = defaultdict(list)
        #self.merged_commits = defaultdict(list)

    """Sets the repo url."""
    def set_repo(self, repo_url):
        self.repo = Repository(repo_url)
        self.process_commits()

    """Retrieves the repo data and adds it to the set."""
    def process_commits(self):
        for commit in self.repo.traverse_commits():
            author = commit.author.name
            if author not in self.author_commits:
                self.author_commits[author] = []

            commit_info = {
                "message": commit.msg,
                "date": commit.author_date.strftime("%Y-%m-%d %H:%M:%S"),
                "files": [{"file_name": mod.filename, "file_path": mod.new_path} for mod in commit.modified_files]
            }

            self.author_commits[author].append(commit_info)
            #self.author_commits[author].append(commit.msg)


    """Saves info to json."""
    def save_to_json(self, filename):
        self.filename = filename
        with open(filename, 'w') as file:
            json.dump(self.author_commits, file, indent=4)

    def print_out_info(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        authors = data.keys()
        print("Authors in repo_data:")
        for author in authors:
            print(author)

    """Gets all authors for the repository."""
    def get_authors(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        authors = data.keys()
        print("Authors:")
        for author in authors:
            print(author)


    """Gets total amount of commits."""
    def get_total_commits(self):
        total_commits = sum(len(commits) for commits in self.author_commits.values())
        print(f"Total commits: {total_commits}")
        return total_commits

    """Gets total amount of commits for contributor."""
    def get_commits_by_author(self, author_name):
        for commit in self.repo.traverse_commits():
            if commit.author.name == author_name:
                print(commit.msg)
