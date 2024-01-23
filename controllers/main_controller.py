class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run_app(self):
        data = self.model.get_data()
        self.view.display_data(data)
