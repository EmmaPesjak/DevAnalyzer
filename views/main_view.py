import customtkinter as ctk
import matplotlib.pyplot as plt
import threading
from tkinter import messagebox
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from support.test_data import total_commits_by_contributor, commit_types_by_contributor, \
    monthly_commits_by_contributor, total_monthly_commits, info_bar_statistics, info_bar_statistics_user
from views.data_visualizer import DataVisualizer

plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#158274", "#3FA27B", "#74C279", "#B2DF74", "#F9F871"])
matplotlib.use('TkAgg')


class MainView:
    MODE_DARK = "dark"
    MODE_LIGHT = "light"
    DEFAULT_THEME = "green"  # blue green or dark-blue
    WINDOW_TITLE = "DevAnalyzer"
    WINDOW_GEOMETRY = "1200x600"
    USERS = ["Anna", "Clara", "Stina"]  # TODO: get this from model when analyzing the repo
    TEXT_COLOR = "#3FA27B"
    PADDING = 10
    mode = MODE_DARK  # Light or dark
    total_commits = 0

    def __init__(self):
        """
        Initializes an instance of the MainView class. This constructor method sets up the main
        application window and its UI components.
        """
        self.visualizer = DataVisualizer(padding=self.PADDING)
        self.root = ctk.CTk()
        self.on_input_change = None
        self.menu_frame = None
        self.diagram_frame = None
        self.git_button = None
        self.user_select = None
        self.mode_button = None
        self.exit_button = None
        self.info_label = None
        self.user_windows = []
        self.setup_appearance()
        self.create_main_window()
        self.setup_ui_components()

    def setup_appearance(self):
        """
        Sets the appearance mode and color theme for the application.
        """
        ctk.set_appearance_mode(self.MODE_DARK)
        ctk.set_default_color_theme(self.DEFAULT_THEME)

    def create_main_window(self):
        """
        Configures the main application window.
        """
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.WINDOW_GEOMETRY)
        self.root.resizable(width=True, height=True)

    def setup_ui_components(self):
        """
        Sets up the user interface components of the application.
        """
        self.setup_layout()
        self.create_sidebar()
        self.create_main_area(initial=True)
        self.create_info_bar(initial=True)

    def setup_layout(self):
        """
        Configures the layout of the main application window.
        """
        self.root.grid_rowconfigure(0, weight=1)  # Make row 0 expandable
        self.root.grid_columnconfigure(0, minsize=200)  # Set min width for column 0 (sidebar)
        self.root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable (main content area)
        self.root.grid_columnconfigure(2, minsize=200)  # Set min width for column 2 (info bar)

    def create_sidebar(self):
        """
        Creates and configures the sidebar with various control buttons.
        """
        self.menu_frame = ctk.CTkFrame(self.root, corner_radius=1)
        self.menu_frame.grid(row=0, column=0, sticky="nswe")  # Expand North, South, West, East

        self.git_button = ctk.CTkButton(self.menu_frame, text="Select repository", command=self.open_git_input)
        self.git_button.grid(row=0, column=0, pady=self.PADDING, padx=self.PADDING, sticky="ew")

        self.mode_button = ctk.CTkButton(self.menu_frame, text="Appearance mode", command=self.set_appearance_mode)
        self.mode_button.grid(row=2, column=0, pady=self.PADDING, padx=self.PADDING, sticky="ew")

        self.exit_button = ctk.CTkButton(self.menu_frame, text="Exit", command=self.on_closing)
        self.exit_button.grid(row=3, column=0, pady=self.PADDING, padx=self.PADDING, sticky="ew")

        # Ensure the application prompts the user before closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_main_area(self, initial=False):
        """
        Creates the main content area of the application where the diagrams are placed.
        """
        self.diagram_frame = ctk.CTkFrame(self.root, corner_radius=1)
        self.diagram_frame.grid(row=0, column=1, sticky="nsew")  # Expand in all directions
        self.diagram_frame.grid_columnconfigure(0, weight=1)
        self.diagram_frame.grid_columnconfigure(1, weight=1)
        self.diagram_frame.grid_rowconfigure(0, weight=1)
        self.diagram_frame.grid_rowconfigure(1, weight=1)

        if initial:
            # Display a placeholder message
            self.placeholder_label = ctk.CTkLabel(self.diagram_frame,
                                                  text="No repository is selected, please select one with the "
                                                       "'Select repository' button.",
                                                  text_color=self.TEXT_COLOR)
            self.placeholder_label.grid(row=0, column=0, sticky="nsew")
        else:
            # Clear the placeholder message and setup diagrams
            if hasattr(self,
                       'placeholder_label') and self.placeholder_label is not None:
                self.placeholder_label.destroy()
            self.setup_overwiew_diagrams()

    def set_total_commits(self, commits):
        self.total_commits = commits
        # TODO update window

    def get_total_commits(self):
        return info_bar_statistics['Most commits']

    def get_most_active_month(self):
        return info_bar_statistics['Most active month']

    def get_most_type_of_commits(self):
        return info_bar_statistics['Most type']

    def get_most_where_of_commits(self):
        return info_bar_statistics['Most changes in']

    # Open the dialog and call the method for input_change
    def open_git_input(self):
        dialog = ctk.CTkInputDialog(text="Enter you repository link:", title="Repository")
        repo_input = dialog.get_input()
        if repo_input and self.on_input_change:
            # Display loading message or indicator
            self.show_loading_indicator()

            # Start the data fetching in a separate thread
            threading.Thread(target=self.fetch_repo_data, args=(repo_input,), daemon=True).start()
            # TODO start thread in the model instead?  handle fetching errors!!!

        else:
            print("No input.")

    def fetch_repo_data(self, repo_input):
        if self.on_input_change:
            self.on_input_change(repo_input)

        # Once data is fetched, update UI on the main thread
        self.root.after(0, self.update_ui_after_fetch)

    def show_loading_indicator(self):
        # Clear existing diagrams
        for widget in self.diagram_frame.winfo_children():
            widget.destroy()

        # Close all user-specific windows
        for window in self.user_windows:
            window.destroy()
        self.user_windows.clear()

        # Clear or reset the info bar
        if hasattr(self, 'info_label') and self.info_label is not None:
            self.info_label.destroy()  # or self.info_label.configure(text="")

        self.loading_label = ctk.CTkLabel(self.diagram_frame, text="Loading, please wait...",
                                          text_color=self.TEXT_COLOR)
        # Place the loading label in a specific row and column, adjust as per your layout needs
        self.loading_label.grid(row=0, column=0, sticky="nsew")

    def update_ui_after_fetch(self):
        # Hide or destroy the loading indicator
        if hasattr(self, 'loading_label') and self.loading_label is not None:
            self.loading_label.destroy()
            self.loading_label = None  # Reset to None to avoid future AttributeError

        # Remove the existing 'user_select' widget if it exists and is not None
        if hasattr(self, 'user_select') and self.user_select is not None:
            self.user_select.destroy()
            self.user_select = None  # Reset to None to ensure it's recognized as destroyed

        # Recreate the 'user_select' widget with potentially updated options
        self.user_select = ctk.CTkOptionMenu(self.menu_frame, values=self.USERS, command=self.setup_user_window)
        self.user_select.set("Select user")
        self.user_select.grid(row=1, column=0, pady=self.PADDING, padx=self.PADDING, sticky="ew")

        # Now, update the main area and info bar
        self.create_main_area()
        self.create_info_bar()

    def create_info_bar(self, initial=False):
        """
        Creates the information bar on to display statistics.
        """
        info_frame = ctk.CTkFrame(self.root, corner_radius=1)
        info_frame.grid(row=0, column=2, sticky="ns")  # Expand only vertically

        if initial:
            pass  # This should be empty when starting the application
        else:
            info_text = (
                f"Total Commits: {self.get_total_commits()}\n"
                f"Most Active Month: {self.get_most_active_month()}\n"
                f"Most Type of Commits: {self.get_most_type_of_commits()}\n"
                f"Most Where of Commits: {self.get_most_where_of_commits()}"
            )
            self.info_label = ctk.CTkLabel(info_frame, text=info_text, text_color=self.TEXT_COLOR)
            self.info_label.pack(pady=10, padx=5, fill='x')

    # Set the callback for changing the repo-input (used from controller)
    def set_on_input_change(self, callback):
        self.on_input_change = callback

    # Acts like a placeholder, is defined in controller.
    def on_input_change(self):
        pass

    def setup_user_window(self, choice):
        new_window = ctk.CTkToplevel(self.root)
        new_window.title(f"Information for {choice}")
        new_window.geometry(self.WINDOW_GEOMETRY)

        # Configure grid layout for new_window
        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_rowconfigure(0, weight=1)

        sidebar_frame = ctk.CTkFrame(new_window, corner_radius=1)
        # Adjust sidebar_frame grid placement
        sidebar_frame.grid(row=0, column=1, sticky="ns")
        new_window.grid_columnconfigure(1, minsize=200)  # Adjust the sidebar width if necessary

        main_area_frame = ctk.CTkFrame(new_window, corner_radius=1)
        main_area_frame.grid(row=0, column=0, sticky="nsew")
        main_area_frame.grid_columnconfigure(0, weight=1)
        main_area_frame.grid_columnconfigure(1, weight=1)
        main_area_frame.grid_rowconfigure(0, weight=1)
        main_area_frame.grid_rowconfigure(1, weight=1)

        fig1, ax1 = self.visualizer.create_figure('bar', data=total_commits_by_contributor, title="What", xlabel="Type",
                                                  ylabel="Commits")
        fig2, ax2 = self.visualizer.create_figure('pie', data=total_commits_by_contributor,
                                                  title="Total commits by contributor")
        fig3, ax3 = self.visualizer.create_figure('line', data=total_monthly_commits, title="Total monthly commits",
                                                  xlabel="Month", ylabel="Commits")
        fig4, ax4 = self.visualizer.create_figure('bar', data=total_commits_by_contributor, title="Where",
                                                  xlabel="Where", ylabel="Commits")

        # Canvas 1
        canvas = FigureCanvasTkAgg(fig1, master=main_area_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Canvas 2
        canvas2 = FigureCanvasTkAgg(fig2, master=main_area_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Canvas 3
        canvas3 = FigureCanvasTkAgg(fig3, master=main_area_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Canvas 4
        canvas4 = FigureCanvasTkAgg(fig4, master=main_area_frame)  # Make sure to use fig4 here instead of fig1
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1, column=1, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Configure grid layout for sidebar_frame to properly align info_label
        sidebar_frame.grid_rowconfigure(0, weight=1)
        info_label = ctk.CTkLabel(sidebar_frame, text=f"Info for {choice} \n {self.create_info_label_text_user()}",
                                  anchor="w", width=130, text_color=self.TEXT_COLOR)
        info_label.grid(row=0, column=0, sticky="nw", padx=self.PADDING, pady=self.PADDING)

        self.user_windows.append(new_window)

        new_window.protocol("WM_DELETE_WINDOW", lambda win=new_window: self.on_user_window_closing(win))

    def on_user_window_closing(self, window):
        # This method is called when a user window is closed
        window.destroy()
        self.user_windows.remove(window)

    def create_info_label_text_user(self):
        info_text = (
            f"Total Commits: {self.get_total_commit_user()}\n"
            f"Most Active Month: {self.get_most_active_month_user()}\n"
            f"Most Type of Commits: {self.get_most_type_of_commits_user()}\n"
            f"Most Where of Commits: {self.get_most_where_of_commits_user()}"
        )
        return info_text

    def get_total_commit_user(self):
        return info_bar_statistics_user['Total commits']

    def get_most_active_month_user(self):
        return info_bar_statistics_user['Most active month']

    def get_most_type_of_commits_user(self):
        return info_bar_statistics_user['What']

    def get_most_where_of_commits_user(self):
        return info_bar_statistics_user['Where']

    def setup_overwiew_diagrams(self):
        fig1, ax1 = self.visualizer.create_figure('bar', data=total_commits_by_contributor,
                                                  title="Total Commits by Contributor",
                                                  xlabel="Contributor", ylabel="Commits")
        fig2, ax2 = self.visualizer.create_figure('pie', data=total_commits_by_contributor,
                                                  title="Total commits by contributor")
        fig3, ax3 = self.visualizer.create_figure('line', data=total_monthly_commits, title="Total Monthly Commits",
                                                  xlabel="Month", ylabel="Commits")
        fig4, ax4 = self.visualizer.create_figure('bar', data=total_commits_by_contributor, title="Where",
                                                  xlabel="Where", ylabel="Commits")

        # Canvas 1
        canvas = FigureCanvasTkAgg(fig1, master=self.diagram_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Canvas 2
        canvas2 = FigureCanvasTkAgg(fig2, master=self.diagram_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Canvas 3
        canvas3 = FigureCanvasTkAgg(fig3, master=self.diagram_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

        # Canvas 4
        canvas4 = FigureCanvasTkAgg(fig4, master=self.diagram_frame)
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1, column=1, padx=self.PADDING, pady=self.PADDING, sticky='nsew')

    def set_appearance_mode(self):
        """
        Toggles the appearance mode of the application between 'dark' and 'light' themes.
        """
        if self.mode == "dark":
            ctk.set_appearance_mode("light")
            self.mode = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.mode = "dark"

    def on_closing(self):
        """
        Handles the closing event of the application.
        """
        if messagebox.askyesno(title="Exit", message="Do you want to exit the application?"):
            self.root.destroy()

    def show_error_message(self, message):
        # TODO fix GUI
        messagebox.showerror("Error", message)
