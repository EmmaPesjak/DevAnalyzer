import customtkinter as ctk
from tkinter import messagebox
import matplotlib
import tkinter as tk

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from support.test_data import total_commits_by_contributor, commit_types_by_contributor, monthly_commits_by_contributor, total_monthly_commits, info_bar_statistics, info_bar_statistics_user
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#158274", "#3FA27B", "#74C279", "#B2DF74", "#F9F871"])

class MainView:

    mode = "dark"
    # Light or dark
    MODE_DARK = "dark"
    MODE_LIGHT = "light"

    # blue green or dark-blue
    DEFAULT_THEME = "green"
    WINDOW_TITLE = "DevAnalyzer"
    WINDOW_GEOMETRY = "1200x600"
    USERS = ["Anna", "Clara", "Stina"]

    def __init__(self):
        self.setup_appearance()
        self.create_main_window()
        self.setup_ui_components()
        self.root.mainloop()

    def setup_appearance(self):
        ctk.set_appearance_mode(self.MODE_DARK)
        ctk.set_default_color_theme(self.DEFAULT_THEME)

    def create_main_window(self):
        self.root = ctk.CTk()
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.WINDOW_GEOMETRY)
        self.root.resizable(width=True, height=True)

    def setup_ui_components(self):
        self.setup_layout()
        self.create_sidebar()
        self.create_main_area()
        self.create_info_bar()

    def setup_layout(self):
        self.root.grid_rowconfigure(0, weight=1)  # Make row 0 expandable
        self.root.grid_columnconfigure(0, minsize=200)  # Set min width for column 0
        self.root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable
        self.root.grid_columnconfigure(2, minsize=200)

    def create_sidebar(self):
        frame1 = ctk.CTkFrame(self.root, corner_radius=1)
        frame1.grid(row=0, column=0, sticky="ns")  # Expand only vertically

        # Add buttons and other components to the sidebar
        self.git_button = ctk.CTkButton(frame1, text="Select repository", command=self.open_git_input)
        self.git_button.pack(pady=5, padx=5)

        self.menubar = ctk.CTkOptionMenu(frame1, values=self.USERS, command=self.setup_user_window)
        self.menubar.set("Select user")
        self.menubar.pack(pady=5, padx=5)

        self.mode_button = ctk.CTkButton(frame1, text="Appearance mode", command=self.set_appearance_mode)
        self.mode_button.pack(pady=5, padx=5)

        self.exit_button = ctk.CTkButton(frame1, text="Exit", command=self.on_closing)
        self.exit_button.pack(pady=5, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_main_area(self):
        self.frame2 = ctk.CTkFrame(self.root, corner_radius=1)
        self.frame2.grid(row=0, column=1, sticky="nsew")  # Expand in all directions

        # TODO fixa sen så att man kan uppdatera i programmet
        self.setup_overwiew_diagrams()

    def create_info_bar(self):
        frame3 = ctk.CTkFrame(self.root, corner_radius=1)
        frame3.grid(row=0, column=2, sticky="ns")  # Expand only vertically

        text_color = "#3FA27B"

        total_commits = "Total Commits: " + str(self.get_total_commits())
        most_active_month = "Most Active Month: " + self.get_most_active_month()
        most_type_of_commits = "Most Type of Commits: " + self.get_most_type_of_commits()
        most_where_of_commits = "Most Where of Commits: " + self.get_most_where_of_commits()

        # Create labels for each statistic
        total_commits_label = ctk.CTkLabel(frame3, text=total_commits, text_color=text_color)
        most_active_month_label = ctk.CTkLabel(frame3, text=most_active_month, text_color=text_color)
        most_type_of_commits_label = ctk.CTkLabel(frame3, text=most_type_of_commits, text_color=text_color)
        most_where_of_commits_label = ctk.CTkLabel(frame3, text=most_where_of_commits, text_color=text_color)

        # Pack the labels with left alignment
        total_commits_label.pack(pady=(10, 2), padx=5)
        most_active_month_label.pack(pady=2, padx=5)
        most_type_of_commits_label.pack(pady=2, padx=5)
        most_where_of_commits_label.pack(pady=2, padx=5)

    def get_total_commits(self):
        return info_bar_statistics['Most commits']

    def get_most_active_month(self):
        return info_bar_statistics['Most active month']

    def get_most_type_of_commits(self):
        return info_bar_statistics['Most type']

    def get_most_where_of_commits(self):
        return info_bar_statistics['Most changes in']

    def open_git_input(self):
        """
        Method for getting a repository. TODO: handle in the model.
        """
        dialog = ctk.CTkInputDialog(text="Enter you repository link:", title="Repository")
        repo_input = dialog.get_input()
        if repo_input:
            print(repo_input)  # TODO The model has to verify that the repo was successfully collected.
        else:
            print("No input.")

    def setup_user_window(self, choice):
        # Create a new Toplevel window
        new_window = ctk.CTkToplevel(self.root)
        new_window.title(f"Information for {choice}")
        new_window.geometry(self.WINDOW_GEOMETRY)  # Adjust the size as needed

        # Create a sidebar in the new window
        sidebar_frame = ctk.CTkFrame(new_window, corner_radius=10)
        sidebar_frame.pack(side="right", fill="y", padx=10, pady=10)

        # Create a main area in the new window
        main_area_frame = ctk.CTkFrame(new_window, corner_radius=10)
        main_area_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # ANTAL COMMITS FÖR VARJE FIX
        fig1, ax1 = plt.subplots(dpi=75)  # dpi sätter size
        ax1.bar(total_commits_by_contributor.keys(), total_commits_by_contributor.values())  # x; name, y; amount
        ax1.set_title("What")
        ax1.set_xlabel("Type")
        ax1.set_ylabel("Commits")

        # PROCENTUELLT VARJE COMMITS PER CONTRIBUTOR
        fig2, ax2 = plt.subplots(dpi=75)  # dpi sätter size
        ax2.pie(total_commits_by_contributor.values(), labels=total_commits_by_contributor.keys(), autopct='%1.1f')
        ax2.set_title("Total commits by contributor")

        # TIMELINE
        fig3, ax3 = plt.subplots(dpi=75)
        ax3.plot(total_monthly_commits.keys(), total_monthly_commits.values())
        ax3.set_title("Total monthly commits")
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Commits")

        # TO BE CHANGED
        fig4, ax4 = plt.subplots(dpi=75)  # dpi sätter size
        ax4.bar(total_commits_by_contributor.keys(), total_commits_by_contributor.values())  # x; name, y; amount
        ax4.set_title("Where")
        ax4.set_xlabel("Where")
        ax4.set_ylabel("Commits")

        main_area_frame.grid_columnconfigure(0, weight=1)
        main_area_frame.grid_columnconfigure(1, weight=1)
        main_area_frame.grid_rowconfigure(0, weight=1)
        main_area_frame.grid_rowconfigure(1, weight=1)

        # Canvas 1
        canvas = FigureCanvasTkAgg(fig1, master=main_area_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Canvas 2
        canvas2 = FigureCanvasTkAgg(fig2, master=main_area_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Canvas 3
        canvas3 = FigureCanvasTkAgg(fig3, master=main_area_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Canvas 4
        canvas4 = FigureCanvasTkAgg(fig4, master=main_area_frame)  # Make sure to use fig4 here instead of fig1
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1, column=1, padx=10, pady=10, sticky='nsew')


        text_color = "#3FA27B"

        user_text = self.create_info_label_text_user()

        # Example sidebar content
        info_label = ctk.CTkLabel(sidebar_frame, text=f"Info for {choice} \n {user_text}", anchor="w", width=130, text_color=text_color)  # Adjust width here
        info_label.pack(padx=10, pady=10, fill='x')  # Ensure label fills the sidebar frame

        # Example main area content
        detail_label = ctk.CTkLabel(main_area_frame, text=f"Details about {choice}'s contributions", anchor="w", text_color=text_color)
        detail_label.pack(padx=10, pady=10)

    def create_info_label_text_user(self):
        total_commits = "Total Commits: " + str(self.get_total_commit_user())
        most_active_month = "Most Active Month: " + self.get_most_active_month_user()
        most_type_of_commits = "Most Type of Commits: " + self.get_most_type_of_commits_user()
        most_where_of_commits = "Most Where of Commits: " + self.get_most_where_of_commits_user()

        total_string = total_commits + "\n" + most_active_month + "\n" + most_type_of_commits + "\n" + most_where_of_commits
        return total_string
        # # Create labels for each statistic
        # total_commits_label = ctk.CTkLabel(frame3, text=total_commits, text_color=text_color)
        # most_active_month_label = ctk.CTkLabel(frame3, text=most_active_month, text_color=text_color)
        # most_type_of_commits_label = ctk.CTkLabel(frame3, text=most_type_of_commits, text_color=text_color)
        # most_where_of_commits_label = ctk.CTkLabel(frame3, text=most_where_of_commits, text_color=text_color)
        #
        # # Pack the labels with left alignment
        # total_commits_label.pack(pady=(10, 2), padx=5)
        # most_active_month_label.pack(pady=2, padx=5)
        # most_type_of_commits_label.pack(pady=2, padx=5)
        # most_where_of_commits_label.pack(pady=2, padx=5)

    def get_total_commit_user(self):
        return info_bar_statistics_user['Total commits']

    def get_most_active_month_user(self):
        return info_bar_statistics_user['Most active month']

    def get_most_type_of_commits_user(self):
        return info_bar_statistics_user['What']

    def get_most_where_of_commits_user(self):
        return info_bar_statistics_user['Where']


    def display_data(self, data):
        print(data)

    def setup_overwiew_diagrams(self):

        # ANTAL COMMITS FÖR VARJE FIX
        fig1, ax1 = plt.subplots(dpi=75) # dpi sätter size
        ax1.bar(total_commits_by_contributor.keys(), total_commits_by_contributor.values())  # x; name, y; amount
        ax1.set_title("What")
        ax1.set_xlabel("Type")
        ax1.set_ylabel("Commits")

        # PROCENTUELLT VARJE COMMITS PER CONTRIBUTOR
        fig2, ax2 = plt.subplots(dpi=75) # dpi sätter size
        ax2.pie(total_commits_by_contributor.values(), labels=total_commits_by_contributor.keys(), autopct='%1.1f')
        ax2.set_title("Total commits by contributor")

        # TIMELINE
        fig3, ax3 = plt.subplots(dpi=75)
        ax3.plot(total_monthly_commits.keys(), total_monthly_commits.values())
        ax3.set_title("Total monthly commits")
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Commits")

        # TO BE CHANGED
        fig4, ax4 = plt.subplots(dpi=75)  # dpi sätter size
        ax4.bar(total_commits_by_contributor.keys(), total_commits_by_contributor.values())  # x; name, y; amount
        ax4.set_title("Where")
        ax4.set_xlabel("Where")
        ax4.set_ylabel("Commits")

        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_rowconfigure(1, weight=1)

        # Canvas 1
        canvas = FigureCanvasTkAgg(fig1, master=self.frame2)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Canvas 2
        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Canvas 3
        canvas3 = FigureCanvasTkAgg(fig3, master=self.frame2)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Canvas 4
        canvas4 = FigureCanvasTkAgg(fig4, master=self.frame2)  # Make sure to use fig4 here instead of fig1
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=1, column=1, padx=10, pady=10, sticky='nsew')


        #plt.show()

    def set_appearance_mode(self):

        if self.mode == "dark":
            ctk.set_appearance_mode("light")
            self.mode = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.mode = "dark"

    def on_closing(self):
        """
        Handle the closing event of the application.
        """
        if messagebox.askyesno(title="Exit", message="Do you want to exit the application?"):
            self.root.destroy()
