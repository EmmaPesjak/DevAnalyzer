class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_on_input_change(self.retrieve_url)

    def run_app(self):
        self.view.root.mainloop()

    # TODO get the input, verify it, and send it to the model
    def retrieve_url(self, new_url):
        self.model.set_repo(new_url)
