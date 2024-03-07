from models.analyzer import Analyzer
from models.batch_analyzer import BatchAnalyzer


class MainController:
    def __init__(self, main_model, view, commit_analyzer):
        self.main_model = main_model
        self.view = view
        self.commit_analyzer = commit_analyzer
        self.view.set_on_input_change(self.retrieve_url)
        #self.commit_test = Analyzer()
        self.analyzer = BatchAnalyzer()

    def retrieve_url(self, new_url):
        self.main_model.cleanup()
        # Pass a callback function to handle the operation's result
        self.main_model.set_repo(new_url, self.handle_set_repo_result)

    def handle_set_repo_result(self, result, error):
        if error:
            # Handle error, possibly in the main thread
            self.view.show_error_message(str(error))
        else:
            # Proceed with UI update or further data processing
            if self.main_model.write_to_file():

                # all_commits = self.main_model.get_all_commits()
                #self.commit_analyzer.nlp(all_commits)
                all_commits = self.main_model.get_all_authors_and_their_commits()
                #self.commit_test.analyze_commits(all_commits)
                self.analyzer.analyze_commits(all_commits)

                self.view.root.after(0, self.view.update_ui_after_fetch)
            else:
                # Handle calculation error
                pass

    # def retrieve_url(self, new_url):
    #     self.main_model.cleanup()
    #     result = self.main_model.set_repo(new_url)
    #
    #     # TODO stop UI update in view
    #     if result != "Success":
    #         self.view.show_error_message(
    #             result)
    #     else:
    #
    #         if self.main_model.calc_data():
    #             self.view.root.after(0, self.view.update_ui_after_fetch)
    #         else:
    #             #Felmeddelande
    #             pass
    #
    #         commits = self.main_model.get_total_amount_of_commits()
    #         #print("Amount of commits: " + str(commits))
    #
    #         contributors = self.main_model.get_all_contributors()
    #         #print("Contributors: " + str(contributors))
    #
    #         most_active_month = self.main_model.get_most_active_month()
    #         #print("Most active month: " + str(most_active_month))
    #
    #         author_info = self.main_model.get_commit_data_with_files_for_author('ebba.nimer@gmail.com')
    #         #print("Commit data for ebba.nimer@gmail.com: " + str(author_info))
    #
    #         activity_info = self.main_model.get_all_months_activity()
    #         print("All months activity: " + str(activity_info))
    #
    #         all_commits = self.main_model.get_all_commits()
    #         #print("All commits: " + str(all_commits))
    #
    #         #print("-----")
    #         self.commit_analyzer.nlp(all_commits)
    #


