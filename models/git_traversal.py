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

    def get_monthly_commits_by_author(self):
        # Initialize variables for the date range
        today = datetime.now()
        twelve_months_ago = today - relativedelta(months=12)

        # Initialize a nested dictionary to count commits by month-year and author
        commits_by_author_and_month = defaultdict(lambda: defaultdict(int))

        # Traverse commits in the repository within the last 12 months
        for commit in self.repo.traverse_commits():
            commit_date = datetime.fromtimestamp(commit.committer_date.timestamp())
            if commit_date >= twelve_months_ago:
                month_year = commit_date.strftime('%Y-%m')
                author_name = commit.author.name
                commits_by_author_and_month[month_year][author_name] += 1

        # Convert the nested dictionary to a list of tuples (month_year, author_name, commits_count)
        results = []
        for month_year, authors in commits_by_author_and_month.items():
            for author_name, commits_count in authors.items():
                results.append((month_year, author_name, commits_count))

        # Sort results by month_year and then by author_name
        results.sort(key=lambda x: (x[0], x[1]))

        return results

    def get_top_files_per_user(self):
        # Initializes a nested dictionary to count file changes by author
        file_changes_by_author = defaultdict(lambda: defaultdict(int))

        # Traverse all commits in the repository
        for commit in self.repo.traverse_commits():
            author_name = commit.author.name
            for modified_file in commit.modified_files:
                file_name = modified_file.filename
                file_changes_by_author[author_name][file_name] += 1

        # Convert the nested dictionary to a sorted list of tuples (author_name, file_name, changes)
        results = []
        for author_name, files in file_changes_by_author.items():
            for file_name, changes in files.items():
                results.append((author_name, file_name, changes))

        # Sort first by author_name, then by changes in descending order
        results.sort(key=lambda x: (x[0], -x[2]))

        return results



