import customtkinter as ctk
from tkinter import messagebox
import matplotlib
import tkinter as tk

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from support.test_data import total_commits_by_contributor, commit_types_by_contributor, monthly_commits_by_contributor, total_monthly_commits
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
    WINDOW_GEOMETRY = "900x600"
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

    def setup_layout(self):
        self.root.grid_rowconfigure(0, weight=1)  # Make row 0 expandable
        self.root.grid_columnconfigure(0, minsize=200)  # Set min width for column 0
        self.root.grid_columnconfigure(1, weight=1)  # Make column 1 expandable

    def create_sidebar(self):
        frame1 = ctk.CTkFrame(self.root, corner_radius=1)
        frame1.grid(row=0, column=0, sticky="ns")  # Expand only vertically

        # Add buttons and other components to the sidebar
        self.git_button = ctk.CTkButton(frame1, text="Select repository", command=self.open_git_input)
        self.git_button.pack(pady=5, padx=5)

        self.menubar = ctk.CTkOptionMenu(frame1, values=self.USERS, command=self.usermenu_callback)
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
        self.setup_diagrams()



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

    def usermenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def display_data(self, data):
        print(data)

    def setup_diagrams(self):

        # ANTAL COMMITS FÖR VARJE CONTRIBUTOR
        fig1, ax1 = plt.subplots(dpi=75) # dpi sätter size
        ax1.bar(total_commits_by_contributor.keys(), total_commits_by_contributor.values())  # x; name, y; amount
        ax1.set_title("Total commits by contributor")
        ax1.set_xlabel("Contributor")
        ax1.set_ylabel("Commits")

        canvas = FigureCanvasTkAgg(fig1, master=self.frame2)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
        #canvas_widget.pack(padx=10, pady=10)  # Adjust padding as needed

        # PROCENTUELLT VARJE COMMITS PER CONTRIBUTOR
        fig2, ax2 = plt.subplots(dpi=75) # dpi sätter size
        ax2.pie(total_commits_by_contributor.values(), labels=total_commits_by_contributor.keys(), autopct='%1.1f')
        ax2.set_title("Total commits by contributor")

        canvas2 = FigureCanvasTkAgg(fig2, master=self.frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(padx=10, pady=10)

        # TIMELINE
        fig3, ax3 = plt.subplots(dpi=75)
        ax3.plot(total_monthly_commits.keys(), total_monthly_commits.values())
        ax3.set_title("Total monthly commits")
        ax3.set_xlabel("Month")
        ax3.set_ylabel("Commits")

        canvas3 = FigureCanvasTkAgg(fig3, master=self.frame2)
        canvas3.draw()
        canvas3.get_tk_widget().pack(padx=10, pady=10)



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
