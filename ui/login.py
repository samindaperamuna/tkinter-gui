from tkinter import W, LEFT, BOTH, E, messagebox, Toplevel
from tkinter.ttk import Frame, Entry, Label, Button

from screen_utils import center_window
from ui.config import Config
from ui.theme import AppStyle


class Login(Frame):
    _username = "Admin"
    _password = "123"

    def __init__(self, parent=None):
        super().__init__(parent)
        parent.bind('<Return>', self.on_login_button_click)

        style = AppStyle()
        style.configure("SELF.TEntry", padding=5)

        self.pack(side=LEFT, fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        username_label = Label(self, text="Username")
        username_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)

        self.username_text = Entry(self, style="SELF.TEntry")
        self.username_text.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=E)

        password_label = Label(self, text="Password")
        password_label.grid(row=1, column=0, padx=[10, 0], pady=[5, 0], sticky=W)

        self.password_text = Entry(self, style="SELF.TEntry", show="*")
        self.password_text.grid(row=1, column=1, padx=[0, 10], pady=[5, 0], sticky=E)

        login_button = Button(self, text="Login")
        login_button.bind("<Button-1>", self.on_login_button_click)
        login_button.grid(row=2, column=1, padx=[0, 10], pady=10, sticky=E)

    def on_login_button_click(self, _):

        if self.validate():
            if self._username.__eq__(self.username_text.get()) and self._password.__eq__(self.password_text.get()):
                # Fetch the main window.
                root = self.master.master

                # Close the login dialog.
                self.master.destroy()

                child = Toplevel(root)
                child.title("Configuration")
                child.geometry("400x235")
                center_window(child)
                child.transient(root)
                child.resizable(False, False)
                child.grab_set()
                Config(child)
            else:
                messagebox.showerror(title="Couldn't Login", message="Invalid username or password.")

    def validate(self):
        if self.username_text.get() == "":
            messagebox.showinfo(title="Missing Required Field", message="Please enter the username.")
            self.username_text.focus_set()
            return False
        elif self.password_text.get() == "":
            messagebox.showinfo(title="Missing Required Field", message="Please enter the password.")
            self.password_text.focus_set()
            return False

        return True
