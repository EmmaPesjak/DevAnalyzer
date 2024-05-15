import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from views.data_visualizer import DataVisualizer
from support import constants
import matplotlib.font_manager
import threading
import textwrap

plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#158274", "#3FA27B", "#74C279", "#B2DF74", "#F9F871", "#FFC185", "#FBA2AE", "#DA9BB7",
           "#B38AAE", "#8C7A9F", "#676A8B", "#2F4858", "#1C6E7D", "#039590"])
plt.rcParams['font.family'] = 'Microsoft YaHei'  # Ensure non-latin characters also can be read.

matplotlib.use('TkAgg')


def wrap_text(text, width=80):
    """
    Wraps the text to a specific width.
    :param text: is the text to wrap.
    :param width: is the width.
    :return: returns the wrapped string.
    """
    return "\n".join(textwrap.wrap(text, width=width))


def open_help():
    """
    Displays a help text.
    """
    messagebox.showinfo(constants.HELP_INFO, constants.HELP_TEXT)


def open_categories():
    """
    Displays a categories text.
    """
    messagebox.showinfo(constants.CAT_INFO, constants.CAT_TEXT)


def read_file_data():
    """
    Read data from a file and return it.
    """
    local_variables = {}
    with open("support//repo_stats.py", 'r', encoding="utf-8") as file:
        file_content = file.read()
        # Execute the file content in an empty global namespace and capture the local variables
        exec(file_content, {}, local_variables)
        return local_variables


class MainView:
    """
    Class responsible for creating the view GUI.
    """
    mode = constants.MODE_DARK  # Light or dark

    def __init__(self):
        """
        Initializes an instance of the MainView class. This constructor method sets up the main
        application window and its UI components.
        """
        self.visualizer = DataVisualizer()
        self.root = ctk.CTk()
        self.repo = None
        self.on_input_change = None
        self.menu_frame = None
        self.diagram_frame = None
        self.help_button = None
        self.categories_button = None
        self.git_button = None
        self.loading_label = None
        self.user_select = None
        self.mode_button = None
        self.exit_button = None
        self.info_label = None
        self.placeholder_label = None
        self.loading_repo = False
        self.user_windows = []
        ctk.set_appearance_mode(constants.MODE_DARK)
        ctk.set_default_color_theme(constants.DEFAULT_THEME)
        self.create_main_window()
        self.setup_ui_components()

    def mainloop(self):
        """
        Starts the main event loop of the tkinter window. The event loop continues running until the window is closed.
        """
        self.root.mainloop()

    def create_main_window(self):
        """
        Configures the main application window.
        """
        self.root.title(constants.WINDOW_TITLE)
        self.root.geometry(constants.WINDOW_GEOMETRY)
        self.root.resizable(width=True, height=True)

    def setup_ui_components(self):
        """
        Sets up the user interface components of the application.
        """
        self.root.grid_rowconfigure(0, weight=1)  # Make row 0 expandable
        self.root.grid_columnconfigure(0, minsize=200)  # Set min width for column 0 (sidebar)
        self.root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable (main content area)
        self.create_sidebar()
        self.create_main_area(initial=True)
        self.create_info_text(initial=True)

    def create_sidebar(self):
        """
        Creates and configures the sidebar with various control buttons.
        """
        self.menu_frame = ctk.CTkFrame(self.root, corner_radius=1)
        self.menu_frame.grid(row=0, column=0, sticky="nswe")

        self.help_button = ctk.CTkButton(self.menu_frame, text=constants.HELP, command=open_help)
        self.help_button.grid(row=0, column=0, pady=constants.PADDING, padx=constants.PADDING, sticky="ew")
        self.categories_button = ctk.CTkButton(self.menu_frame, text=constants.CATEGORIES, command=open_categories)
        self.categories_button.grid(row=1, column=0, pady=constants.PADDING, padx=constants.PADDING, sticky="ew")
        self.git_button = ctk.CTkButton(self.menu_frame, text=constants.SELECT_REPO, command=self.open_git_input)
        self.git_button.grid(row=2, column=0, pady=constants.PADDING, padx=constants.PADDING, sticky="ew")
        self.mode_button = ctk.CTkButton(self.menu_frame, text=constants.APP_MODE, command=self.set_appearance_mode)
        self.mode_button.grid(row=4, column=0, pady=constants.PADDING, padx=constants.PADDING, sticky="ew")
        self.exit_button = ctk.CTkButton(self.menu_frame, text=constants.EXIT, command=self.on_closing)
        self.exit_button.grid(row=5, column=0, pady=constants.PADDING, padx=constants.PADDING, sticky="ew")

        # Ensure the application prompts the user before closing.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_main_area(self, file_data=None, initial=False):
        """
        Creates the main content area of the application where the diagrams are placed.
        :param file_data: Data to generate the diagrams.
        :param initial: Flag indicating if the placeholder label should be displayed.
        """
        if self.diagram_frame:
            self.diagram_frame.destroy()

        self.diagram_frame = ctk.CTkScrollableFrame(self.root)
        self.diagram_frame.grid(row=0, column=1, sticky="nsew")
        self.diagram_frame.grid_columnconfigure(0, weight=1)
        self.diagram_frame.grid_columnconfigure(1, weight=1)
        self.diagram_frame.grid_rowconfigure(0, weight=1)
        self.diagram_frame.grid_rowconfigure(1, weight=1)
        self.diagram_frame.grid_rowconfigure(2, weight=1)
        self.diagram_frame.grid_rowconfigure(3, weight=1)

        if initial:
            # Display a placeholder message.
            self.show_init_label()
        else:
            # Clear the placeholder message and setup diagrams.
            if hasattr(self,
                       'placeholder_label') and self.placeholder_label is not None:
                self.placeholder_label.destroy()
            self.setup_overwiew_diagrams(file_data)

    def show_init_label(self):
        """
        Displays a loading label in the diagram frame.
        """
        self.placeholder_label = ctk.CTkLabel(self.diagram_frame, text=constants.SELECT_REPO_TEXT,
                                              text_color=constants.TEXT_COLOR, font=("Segoe UI", 16, "bold"))
        self.placeholder_label.grid(row=0, column=0, sticky="nsew")

    def open_git_input(self):
        """
        Opens a dialog box for the user to enter a GitHub repository link. Upon receiving input,
        it displays a loading indicator and initiates the process of fetching repository data.
        """
        dialog = ctk.CTkInputDialog(text=constants.ENTER_REPO, title=constants.REPO)
        repo_input = dialog.get_input()
        if repo_input and self.on_input_change:
            # Schedule the loading indicator to show in the main GUI thread.
            self.root.after(0, self.show_loading_indicator)
            # Start a thread to fetch repository data.
            thread = threading.Thread(target=self.fetch_repo_data, args=(repo_input,))
            thread.start()
            self.loading_repo = True

    def fetch_repo_data(self, repo_input):
        """
        Initiates the process of fetching repository data. It triggers the `on_input_change`
        callback with the provided repository URL.
        """
        if self.on_input_change:
            self.on_input_change(repo_input)

    def set_on_input_change(self, callback):
        """
        Registers a callback function to be invoked when the repository URL input changes.
        """
        self.on_input_change = callback

    def on_input_change(self):
        """
        A placeholder method meant to be overridden by `set_on_input_change`.
        """
        pass

    def remove_loading_indicator(self):
        """
        Destroy the loading indicator.
        """
        if hasattr(self, 'loading_label') and self.loading_label is not None:
            self.loading_label.destroy()
            self.loading_label = None  # Reset to None to avoid future AttributeError.

    def remove_user_select(self):
        """
        Destroy the user select.
        """
        if hasattr(self, 'user_select') and self.user_select is not None:
            self.user_select.destroy()
            self.user_select = None  # Reset to None to ensure it's recognized as destroyed.

    def show_loading_indicator(self):
        """
        Clears the UI and displays a loading indicator in the UI and prepares the interface for data loading.
        """
        # Clear existing diagrams.
        for widget in self.diagram_frame.winfo_children():
            widget.destroy()

        # Close all user-specific windows.
        for window in self.user_windows:
            window.destroy()
        self.user_windows.clear()

        # Clear or reset the info bar.
        if hasattr(self, 'info_label') and self.info_label is not None:
            self.info_label.destroy()  # or self.info_label.configure(text="")

        self.loading_label = ctk.CTkLabel(self.diagram_frame, text=constants.LOADING,
                                          text_color=constants.TEXT_COLOR, font=("Segoe UI", 16, "bold"))
        # Place the loading label in a specific row and column.
        self.loading_label.grid(row=0, column=0, sticky="nsew")

    def update_ui_after_fetch(self, repo):
        """
        Updates the UI elements after data fetching is complete.
        """
        # Destroy the loading indicator
        self.remove_loading_indicator()
        self.loading_repo = False

        self.repo = repo

        # Remove the existing 'user_select' widget if it exists and is not None.
        self.remove_user_select()

        file_data = read_file_data()
        total_commits_by_contributor = file_data['total_commits_by_contributor']

        # Create a list of the users.
        users = list(total_commits_by_contributor.keys())

        # Recreate the 'user_select' widget with potentially updated options.
        self.user_select = ctk.CTkOptionMenu(self.menu_frame, values=users,
                                             command=lambda choice: self.setup_user_window(choice, file_data))
        self.user_select.set(constants.SELECT_USER)
        self.user_select.grid(row=3, column=0, pady=constants.PADDING, padx=constants.PADDING, sticky="ew")

        # Update the main area and info bar.
        self.create_main_area(file_data)
        self.create_info_text(file_data)

    def create_info_text(self, file_data=None, initial=False):
        """
        Creates the information bar on to display statistics.
        :param file_data: Data to generate text.
        :param initial: Flag indicating if the bar should be empty.
        """
        if initial:
            pass  # This should be empty when starting the application.
        else:
            # Verify data presence and non-emptiness for required keys.
            if 'total_commits_by_contributor' in file_data and file_data['total_commits_by_contributor']:
                total_commits = sum(file_data['total_commits_by_contributor'].values())
            else:
                total_commits = 0

            if 'readme_summary' in file_data:
                readme_summary = file_data['readme_summary']
            else:
                readme_summary = constants.NONE
            readme_summary = wrap_text(readme_summary, width=120)

            if 'overall_summary' in file_data:
                overall_summary = file_data['overall_summary']
            else:
                overall_summary = constants.NONE
            overall_summary = wrap_text(overall_summary, width=120)

            info_text = (
                f"Total number of commits: {total_commits}\n\n"
                f"Overall summary: \n{overall_summary}\n\n"
                f"Readme summary:\n{readme_summary}"
            )
            self.info_label = ctk.CTkLabel(self.diagram_frame, text=info_text, text_color=constants.TEXT_COLOR)
            self.info_label.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def setup_user_window(self, choice, file_data):
        """
        Sets ut the user window with diagrams and info text.
        :param choice: The name of the user choice.
        :param file_data: Data to generate text.
        """
        new_window = ctk.CTkToplevel(self.root)
        new_window.title(f"Information about {choice}")
        new_window.geometry(constants.WINDOW_GEOMETRY)

        # Configure the window to expand the frame to full window.
        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)

        main_area_frame = ctk.CTkScrollableFrame(new_window)
        main_area_frame.grid(row=0, column=0, sticky="nsew")
        main_area_frame.grid_columnconfigure(0, weight=1)
        main_area_frame.grid_columnconfigure(1, weight=1)
        main_area_frame.grid_rowconfigure(0, weight=1)
        main_area_frame.grid_rowconfigure(1, weight=1)

        # Initialize info_text with basic information.
        info_text_parts = [f"Info for {choice}"]

        # Track if any data was found.
        data_found = False

        # Check and create total commits by contributor.
        if choice in file_data.get('total_commits_by_contributor', {}):
            data_found = True
            total_commits_for_user = file_data['total_commits_by_contributor'][choice]
            info_text_parts.append(f"Total Commits: {total_commits_for_user}")

        # Check and create a diagram for types per user.
        if choice in file_data.get('total_what_per_user', {}):
            data_found = True
            types_per_user = file_data['total_what_per_user'][choice]
            fig1, ax1 = self.visualizer.create_figure('spider', data=types_per_user, title="Type of commit")
            # Canvas 1
            canvas = FigureCanvasTkAgg(fig1, master=main_area_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, padx=constants.PADDING, pady=constants.PADDING, sticky='nsew')

        # Check and create a diagram for top 10 changed files per user.
        if choice in file_data.get('total_where_per_user', {}):
            data_found = True
            top_10_per_user = file_data['total_where_per_user'][choice]

            fig4, ax4 = self.visualizer.create_figure('spider', data=top_10_per_user,
                                                      title="Where the commits has been made")
            # Canvas 4
            canvas4 = FigureCanvasTkAgg(fig4, master=main_area_frame)
            canvas4.draw()
            canvas4.get_tk_widget().grid(row=1, column=1, padx=constants.PADDING, pady=constants.PADDING, sticky='nsew')

        if choice in file_data.get('personal_summaries', {}):
            data_found = True
            personal_summary = file_data['personal_summaries'][choice]
            personal_summary = wrap_text(personal_summary, width=120)
            info_text_parts.append(f"Personal Summary:\n{personal_summary}")

        if not data_found:
            # If no data was found for any category.
            info_text = f"The user {choice} has not committed enough to analyze."
        else:
            info_text = "\n\n".join(info_text_parts)

        info_label = ctk.CTkLabel(main_area_frame, text=info_text,
                                  anchor="center", width=120, text_color=constants.TEXT_COLOR)
        info_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=constants.PADDING, pady=constants.PADDING)
        self.user_windows.append(new_window)
        new_window.protocol("WM_DELETE_WINDOW", lambda win=new_window: self.on_user_window_closing(win))

    def on_user_window_closing(self, window):
        """
        This method is called when a user window is closed.
        :param window: The current window to destroy.
        """
        window.destroy()
        self.user_windows.remove(window)

    def setup_overwiew_diagrams(self, file_data):
        """
        Sets up the overview diagrams.
        :param file_data: Data to generate the diagrams.
        """
        repo_label = ctk.CTkLabel(self.diagram_frame, text=self.repo, text_color=constants.TEXT_COLOR)
        repo_label.grid(row=0, column=0, columnspan=2, padx=constants.PADDING, pady=constants.PADDING, sticky='nsew')

        # Initialize a flag to keep track of whether any diagrams were created.
        diagrams_created = False
        diagram_row = 2  # Start placing diagrams after the repository label row

        # Check for 'types_of_commits' data and create a diagram if it's not empty.
        if 'total_what' in file_data and file_data['total_what']:
            diagrams_created = True
            fig1, ax1 = self.visualizer.create_figure('spider', data=file_data['total_what'],
                                                      title="Type of commit")
            canvas1 = FigureCanvasTkAgg(fig1, master=self.diagram_frame)
            canvas1.draw()
            canvas1.get_tk_widget().grid(row=diagram_row, column=0, padx=constants.PADDING, pady=constants.PADDING,
                                         sticky='nsew')

        # Check for 'total_commits_by_contributor' data and create a diagram if it's not empty.
        if 'total_commits_by_contributor' in file_data and file_data['total_commits_by_contributor']:
            diagrams_created = True
            fig2, ax2 = self.visualizer.create_figure('pie', data=file_data['total_commits_by_contributor'],
                                                      title="Commits by contributors")
            canvas2 = FigureCanvasTkAgg(fig2, master=self.diagram_frame)
            canvas2.draw()
            canvas2.get_tk_widget().grid(row=diagram_row+1, column=0, padx=constants.PADDING, pady=constants.PADDING,
                                         sticky='nsew')

        # Check for 'total_where' data and create a diagram if it's not empty.
        if 'total_where' in file_data and file_data['total_where']:
            diagrams_created = True
            fig4, ax4 = self.visualizer.create_figure('spider', data=file_data['total_where'],
                                                      title="Where the commits has been made")
            canvas4 = FigureCanvasTkAgg(fig4, master=self.diagram_frame)
            canvas4.draw()
            canvas4.get_tk_widget().grid(row=diagram_row, column=1, padx=constants.PADDING, pady=constants.PADDING,
                                         sticky='nsew')

        # If no diagrams were created due to empty datasets.
        if not diagrams_created:
            no_data_label = ctk.CTkLabel(self.diagram_frame, text=constants.NO_DATA, text_color=constants.TEXT_COLOR)
            no_data_label.grid(row=0, column=0, padx=constants.PADDING, pady=constants.PADDING, sticky='nsew')

    def set_appearance_mode(self):
        """
        Toggles the appearance mode of the application between 'dark' and 'light' themes.
        """
        if self.mode == constants.MODE_DARK:
            ctk.set_appearance_mode(constants.MODE_LIGHT)
            self.mode = constants.MODE_LIGHT
        else:
            ctk.set_appearance_mode(constants.MODE_DARK)
            self.mode = constants.MODE_DARK

    def on_closing(self):
        """
        Handles the closing event of the application.
        """
        if self.loading_repo:
            # Check if the user really wants to exit while loading.
            if messagebox.askyesno(constants.EXIT, constants.LOADING_IN_PROG):
                self.root.quit()
        else:
            # Normal exit prompt.
            if messagebox.askyesno(title=constants.EXIT, message=constants.EXIT_Q):
                self.root.quit()

    def show_error_message(self, message):
        """
        Shows error messages in a message box.
        """
        self.loading_repo = False
        messagebox.showerror(constants.ERROR, message)
