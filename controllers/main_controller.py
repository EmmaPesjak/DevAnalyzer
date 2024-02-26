class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_on_input_change(self.retrieve_url)

    def run_app(self):
        self.view.root.mainloop()

    # TODO get the input, verify it, and send it to the model
    def retrieve_url(self, new_url):
        self.model.cleanup()
        self.model.set_repo(new_url)
        commits = self.model.get_total_amount_of_commits()
        print("Amount of commits: " + str(commits))

        contributors = self.model.get_all_contributors()
        print("Contributors: " + str(contributors))

        most_active_month = self.model.get_most_active_month()
        print("Most active month: " + str(most_active_month))

        author_info = self.model.get_commit_data_with_files_for_author('ebba.nimer@gmail.com')
        print(str(author_info))

        activity_info = self.model.get_all_months_activity()
        print(str(activity_info))
