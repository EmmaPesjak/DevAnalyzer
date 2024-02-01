import customtkinter
import customtkinter as ctk
from tkinter import messagebox

class MainView:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("DevAnalyzer")
        self.root.geometry("900x600")
        self.root.resizable(width=True, height=True)

        self.root.grid_rowconfigure(0, weight=1)  # This makes the row 0 expandable (fills the height).

        self.root.grid_columnconfigure(0, minsize=200)  # This sets the minimum width for column 0 to 200.
        self.root.grid_columnconfigure(1, weight=1)  # This makes column 1 expandable (fills the rest of the width).

        frame1 = customtkinter.CTkFrame(self.root, border_width=5, border_color="gray", fg_color="blue")
        frame1.grid(row=0, column=0, sticky="ns")  # 'ns' makes it expand only vertically.

        frame2 = customtkinter.CTkFrame(self.root, fg_color="red")
        frame2.grid(row=0, column=1, sticky="nsew")  # 'nsew' makes it expand in all directions.

        users = ["Anna", "Clara", "Stina"]
        self.menubar = ctk.CTkOptionMenu(frame1, values=users, command=self.usermenu_callback)
        self.menubar.set("Options")
        self.menubar.pack()

        # Exit button.
        self.exit_button = ctk.CTkButton(frame1, text="Exit", command=self.on_closing)
        self.exit_button.pack()

        # Exit handling.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Mainloop.
        self.root.mainloop()

    def usermenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)

    def display_data(self, data):
        print(data)

    def on_closing(self):
        """
        Handle the closing event of the application.
        """
        if messagebox.askyesno(title="Exit", message="Do you want to exit the application?"):
            self.root.destroy()
