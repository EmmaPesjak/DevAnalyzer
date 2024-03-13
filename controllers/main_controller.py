from models.batch_analyzer import BatchAnalyzer
import time


class MainController:
    """
    The main controller of the application.
    """

    def __init__(self, main_model, view):
        """
        Initialization of the controller.
        :param main_model: The model to calculate/analyze data.
        :param view: The view to present data.
        """
        self.repo = None
        self.main_model = main_model
        self.view = view
        self.view.set_on_input_change(self.retrieve_url)
        self.analyzer = BatchAnalyzer()

    def retrieve_url(self, new_url):
        """
        Sets a new repository URL and initiates its cleanup and setup.
        :param new_url: URL to set as the new repository.
        """
        self.repo = new_url
        self.start_time = time.time()  # Start timing, remove this later.
        self.main_model.cleanup()
        self.main_model.set_repo(new_url, self.handle_set_repo_result)

    def handle_set_repo_result(self, result, error):
        """
        Handles the outcome of setting a new repository URL.
        :param result: The result of the repository setup attempt.
        :param error: Any error that occurred during repository setup.
        """
        if error:
            # Handle error, possibly in the main thread
            self.view.remove_loading_indicator()
            self.view.remove_user_select()
            self.view.show_init_label()
            self.view.show_error_message("Was not able to get the repository, please try again,"
                                         " make sure to enter a valid Git repository URL.")
            # self.view.show_error_message(str(error))
        else:
            # Proceed with UI update or further data processing
            if self.main_model.write_to_file():
                all_commits = self.main_model.get_all_authors_and_their_commits()
                self.analyzer.analyze_commits(all_commits)
                # If the timer is removed, change end_timing to self.view.update_ui_after_fetch
                self.view.root.after(0, self.end_timing)
            else:
                self.view.show_error_message("Something went wrong, please try again")

    def end_timing(self):
        """
        Helper method to see how long time it takes to execute.
        """
        self.view.update_ui_after_fetch(self.repo)  # Call the original update function
        end_time = time.time()  # Stop timing
        duration = end_time - self.start_time  # Calculate duration
        print(f"Total time taken: {duration} seconds")
