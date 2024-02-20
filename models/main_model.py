from pydriller import Repository

for commit in Repository("https://github.com/EmmaPesjak/DevAnalyzer").traverse_commits():
    print("Author: " + commit.author.name + ", msg: " + commit.msg)

class MainModel:

    def get_data(self):
        return "Hi from the Model!"
