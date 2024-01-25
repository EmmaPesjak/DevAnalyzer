import customtkinter as ctk

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

        self.root.mainloop()


    def display_data(self, data):
        print(data)
