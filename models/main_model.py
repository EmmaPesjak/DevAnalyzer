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

    def __init__(self):
        self.repo = None
        self.author_commits = {}  # Store authors and their commits
        self.author_commits = defaultdict(list)

    """Sets the repo url."""
    def set_repo(self, repo_url):
        self.repo = Repository(repo_url)
        self.process_commits()

    """Retrieves the repo data and adds it to the set."""
    def process_commits(self):
        for commit in self.repo.traverse_commits():
            if not commit.merge:  # Ignore merge commits
                self.author_commits[commit.author.name].append(commit.msg.strip())

        # for commit in self.repo.traverse_commits():
        #     author_email = commit.author.email.lower()  # Using email as unique identifier
        #     if author_email not in self.author_commits:
        #         self.author_commits[author_email] = []
        #     self.author_commits[author_email].append(commit.msg)

    def filter_contributors(self):
        # Filter out contributors who don't have non-merge commits
        self.author_commits = {author: commits for author, commits in self.author_commits.items() if commits}

    def get_total_commits(self):
        total_commits = sum(len(commits) for commits in self.author_commits.values())
        return total_commits

    """Saves info to json."""
    def save_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.author_commits, file, indent=4)






    """Gets all authors for the repository."""
    def get_authors(self):
        for commit in self.repo.traverse_commits():

            author_identity = commit.author.email.lower()  # Using email as a unique identifier
            self.authors.add(author_identity)

        print(list(self.authors))

    """Gets total amount of commits."""
    def get_total_amount_of_commits(self):
        metric = CommitsCount(path_to_repo=self.repo)
        files = metric.count()
        print('Files: {}'.format(files))
        pass

    """Gets total amount of commits for contributor."""
    def get_commits_by_author(self, author_name):
        for commit in self.repo.traverse_commits():
            if commit.author.name == author_name:
                print(commit.msg)

    def get_data(self):
        return "Hi from the Model!"
