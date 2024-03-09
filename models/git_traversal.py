import time

from dateutil.relativedelta import relativedelta
from pydriller import Repository, repository
import calendar
from datetime import datetime, timedelta
from collections import defaultdict
from dateutil.relativedelta import relativedelta

class GitTraversal:

    def __init__(self):
        self.repo = None

    def set_repo(self, repo_url):
        self.repo = repository.Repository(repo_url)

    def get_authors_with_amount_of_commits(self):
        total_commits_by_contributor = {}

        for commit in self.repo.traverse_commits():
            author_name = commit.author.name
            if author_name in total_commits_by_contributor:
                total_commits_by_contributor[author_name] += 1
            else:
                total_commits_by_contributor[author_name] = 1

        return total_commits_by_contributor

    def get_all_authors_and_their_commits(self):
        """
        Retrieves all authors along with their commit messages directly from the git repository.
        """
        authors_commits = {}

        for commit in self.repo.traverse_commits():
            author_name = commit.author.name
            commit_message = commit.msg.strip()

            if author_name not in authors_commits:
                authors_commits[author_name] = []
            authors_commits[author_name].append(commit_message)

        return authors_commits

    def get_commit_counts_past_year(self):
        # Initialize counters for each month of the past year
        today = datetime.now()
        twelve_months_ago = today - relativedelta(months=12)
        commit_counts = defaultdict(int)

        # Iterate through commits from the last 12 months
        for commit in self.repo.traverse_commits():
            commit_date = datetime.fromtimestamp(commit.committer_date.timestamp())
            if commit_date >= twelve_months_ago:
                month_year = commit_date.strftime('%Y-%m')
                commit_counts[month_year] += 1

        # Ensure all months are represented, even those without commits
        structured_data = {}
        for i in range(12):
            month = (today - relativedelta(months=i)).strftime("%Y-%m")
            structured_data[month] = commit_counts.get(month, 0)

        return structured_data



