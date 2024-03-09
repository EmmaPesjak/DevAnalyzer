from models.batch_analyzer import BatchAnalyzer
import time

class MainController:
    def __init__(self, main_model, view, commit_analyzer):
        self.main_model = main_model
        self.view = view
        self.commit_analyzer = commit_analyzer
        self.view.set_on_input_change(self.retrieve_url)
        self.analyzer = BatchAnalyzer()

    def retrieve_url(self, new_url):
        self.start_time = time.time()  # Start timing
        self.main_model.cleanup()
        self.main_model.set_repo(new_url, self.handle_set_repo_result)

    def handle_set_repo_result(self, result, error):
        if error:
            # Handle error, possibly in the main thread
            self.view.remove_loading_indicator()
            self.view.remove_user_select()
            self.view.show_init_label()
            self.view.show_error_message(str(error))
        else:
            # Proceed with UI update or further data processing
            if self.main_model.write_to_file():
                all_commits = self.main_model.get_all_authors_and_their_commits()
                self.analyzer.analyze_commits(all_commits)
                self.view.root.after(0, self.end_timing)  # Modify to call end_timing after update

    def end_timing(self):
        self.view.update_ui_after_fetch()  # Call the original update function
        end_time = time.time()  # Stop timing
        duration = end_time - self.start_time  # Calculate duration
        print(f"Time taken: {duration} seconds") 
