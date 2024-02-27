from controllers.main_controller import MainController
from views.main_view import MainView
from models.main_model import MainModel
from models.commit_analyzer import CommitAnalyzer


def main():
    main_model = MainModel()
    view = MainView()
    commit_analyzer = CommitAnalyzer()
    controller = MainController(main_model, view, commit_analyzer)
    controller.run_app()

if __name__ == "__main__":
    main()

