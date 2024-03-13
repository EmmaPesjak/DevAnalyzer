from pydriller import Repository, repository


class GitTraversal:
    """
    Facilitates traversal and analysis of a Git repository using PyDriller.
    """

    def __init__(self):
        """
        Initializes the GitTraversal object with no repository set.
        """
        self.repo_url = None
        self.repo = None

    def set_repo(self, repo_url):
        """
        Sets the repository to the specified URL and initializes the Repository object.
        :param repo_url: The URL of the Git repository.
        :return: A string indicating "Success" or an error message if the repository cannot be set.
        """
        try:
            self.repo = repository.Repository(repo_url)
            self.repo_url = repo_url
        except Exception as e:
            error_message = "Please try again with an existing repository."
        else:
            return "Success"
        return error_message

    def get_authors_with_amount_of_commits(self):
        """
        Computes the number of commits made by each author in the repository.
        :return: A dictionary mapping author names to their respective commit counts.
        """
        total_commits_by_contributor = {}

        for commit in self.repo.traverse_commits():
            author_name = commit.author.name
            if author_name in total_commits_by_contributor:
                total_commits_by_contributor[author_name] += 1
            else:
                total_commits_by_contributor[author_name] = 1

        return total_commits_by_contributor
