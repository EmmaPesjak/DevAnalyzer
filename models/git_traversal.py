from pydriller import Repository, repository


class GitTraversal:

    def __init__(self):
        self.repo_url = None
        self.repo = None

    def set_repo(self, repo_url):
        try:
            self.repo = repository.Repository(repo_url)
            self.repo_url = repo_url
        except Exception as e:
            error_message = "Please try again with an existing repository."
        else:
            return "Success"
        return error_message

    def get_authors_with_amount_of_commits(self):
        total_commits_by_contributor = {}

        for commit in self.repo.traverse_commits():
            author_name = commit.author.name
            if author_name in total_commits_by_contributor:
                total_commits_by_contributor[author_name] += 1
            else:
                total_commits_by_contributor[author_name] = 1

        return total_commits_by_contributor
