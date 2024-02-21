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
        self.model.save_to_json('repo_data.json')
        self.model.get_total_commits()
        #self.model.save_to_json('repo_data.json')
        #self.model.get_authors()
        #self.model.get_commits_by_author('ebbanimer')
        #self.model.get_total_amount_of_commits()
        #print(new_url)
