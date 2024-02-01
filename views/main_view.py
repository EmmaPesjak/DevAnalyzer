import customtkinter as ctk
from tkinter import messagebox



class MainView:

    #global mode
    mode = "dark"

    def __init__(self):

        ctk.set_appearance_mode("dark")  # Light or dark
        ctk.set_default_color_theme("green")  # blue green or dark-blue


        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("DevAnalyzer")
        self.root.geometry("900x600")
        self.root.resizable(width=True, height=True)



        self.root.grid_rowconfigure(0, weight=1)  # This makes the row 0 expandable (fills the height).

        self.root.grid_columnconfigure(0, minsize=200)  # This sets the minimum width for column 0 to 200.
        self.root.grid_columnconfigure(1, weight=1)  # This makes column 1 expandable (fills the rest of the width).

        frame1 = ctk.CTkFrame(self.root, corner_radius=1)
        frame1.grid(row=0, column=0, sticky="ns")  # 'ns' makes it expand only vertically.

        frame2 = ctk.CTkFrame(self.root, corner_radius=1)
        frame2.grid(row=0, column=1, sticky="nsew")  # 'nsew' makes it expand in all directions.

        self.git_button = ctk.CTkButton(frame1, text="Select repository", command=self.open_git_input)
        self.git_button.pack(pady=5, padx=5)

        users = ["Anna", "Clara", "Stina"]
        self.menubar = ctk.CTkOptionMenu(frame1, values=users, command=self.usermenu_callback)
        self.menubar.set("Select user")
        self.menubar.pack(pady=5, padx=5)

        # Mode button
        self.mode_button = ctk.CTkButton(frame1, text="Appearance mode", command=self.set_appearance_mode)
        self.mode_button.pack(pady=5, padx=5)

        # Exit button.
        self.exit_button = ctk.CTkButton(frame1, text="Exit", command=self.on_closing)
        self.exit_button.pack(pady=5, padx=5)

        # Exit handling.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Mainloop.
        self.root.mainloop()

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
