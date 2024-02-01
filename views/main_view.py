import customtkinter as ctk
from tkinter import messagebox

class MainView:
    def __init__(self):
        self.root = ctk.CTk()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("DevAnalyzer")
        self.root.geometry("900x600")
        self.menubar = ctk.CTkOptionMenu(self.root, values=["Test1", "Test2", "Test3"])
        self.menubar.set("Options")
        self.menubar.pack()

        # Exit button.
        self.exit_button = ctk.CTkButton(self.root, text="Exit", command=self.on_closing)
        self.exit_button.pack()

        # Exit handling.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Mainloop.
        self.root.mainloop()


    def display_data(self, data):
        print(data)

    def on_closing(self):
        """
        Handle the closing event of the application.
        """
        if messagebox.askyesno(title="Exit", message="Do you want to exit the application?"):
            self.root.destroy()
