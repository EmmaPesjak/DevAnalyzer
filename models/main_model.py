from pydriller import Repository
from urllib3.util import url


class MainModel:

    def __init__(self):
        self.repo = None

    def set_repo(self, url):
        self.repo = Repository(url)

    def retrieve_repository(self, url):
        for commit in Repository(url).traverse_commits():
            print("Author: " + commit.author.name + ", msg: " + commit.msg)

    def get_authors(self):
        for commit in self.repo.traverse_commits():
            print("Author: " + commit.author.name)


    def get_data(self):
        return "Hi from the Model!"
