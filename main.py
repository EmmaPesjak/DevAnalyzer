from controllers.main_controller import MainController
from views.main_view import MainView
from models.main_model import MainModel


def main():
    """
    Main starting point of the application.
    """
    main_model = MainModel()
    view = MainView()
    controller = MainController(main_model, view)
    view.mainloop()


if __name__ == "__main__":
    main()

