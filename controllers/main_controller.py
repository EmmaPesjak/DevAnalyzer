class MainController:
    def __init__(self, main_model, view, commit_analyzer):
        self.main_model = main_model
        self.view = view
        self.commit_analyzer = commit_analyzer
        self.view.set_on_input_change(self.retrieve_url)

    def run_app(self):
        self.view.root.mainloop()

    # TODO get the input, verify it, and send it to the model

    def retrieve_url(self, new_url):
        self.main_model.cleanup()
        result = self.main_model.set_repo(new_url)

        # TODO stop UI update in view
        if result != "Success":
            self.view.show_error_message(
                result)
        else:
            commits = self.main_model.get_total_amount_of_commits()
            print("Amount of commits: " + str(commits))

            contributors = self.main_model.get_all_contributors()
            print("Contributors: " + str(contributors))

            most_active_month = self.main_model.get_most_active_month()
            print("Most active month: " + str(most_active_month))

            author_info = self.main_model.get_commit_data_with_files_for_author('ebba.nimer@gmail.com')
            print("Commit data for ebba.nimer@gmail.com: " + str(author_info))

            activity_info = self.main_model.get_all_months_activity()
            print("All months activity: " + str(activity_info))

            all_commits = self.main_model.get_all_commits()
            print("All commits: " + str(all_commits))

            print("-----")
            self.commit_analyzer.preprocess_data(all_commits)
