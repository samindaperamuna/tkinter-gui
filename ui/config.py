from tkinter import LEFT, BOTH, E, W, N, messagebox, END
from tkinter.ttk import Frame, Notebook, Label, Entry, Button

from data.json_util import read_settings, write_settings, reset_default
from ui.theme import AppStyle


class Config(Frame):
    data = None

    def __init__(self, parent=None):
        super().__init__(parent)
        parent.bind('<Return>', self.on_accept_button_click)

        self.pack(side=LEFT, fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        style = AppStyle()
        style.configure("SELF.TLabel", width=15)
        style.configure("SELF.TEntry", width=200, padding=5)

        # Tab container.
        notebook = Notebook(self)

        # Main tab content
        main = Frame(notebook)
        main.columnconfigure(1, weight=1)

        screen_label = Label(main, text="Screen", style="SELF.TLabel")
        screen_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.screen_entry = Entry(main, style="SELF.TEntry")
        self.screen_entry.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        width_label = Label(main, text="Width percent", style="SELF.TLabel")
        width_label.grid(row=1, column=0, padx=[10, 0], pady=[5, 0], sticky=W)
        self.width_entry = Entry(main, style="SELF.TEntry")
        self.width_entry.grid(row=1, column=1, padx=[0, 10], pady=[5, 0], sticky=W + E)

        height_label = Label(main, text="Height percent", style="SELF.TLabel")
        height_label.grid(row=2, column=0, padx=[10, 0], pady=[5, 0], sticky=W)
        self.height_entry = Entry(main, style="SELF.TEntry")
        self.height_entry.grid(row=2, column=1, padx=[0, 10], pady=[5, 0], sticky=W + E)

        camera_type_label = Label(main, text="Camera type", style="SELF.TLabel")
        camera_type_label.grid(row=3, column=0, padx=[10, 0], pady=[5, 10], sticky=W)
        self.camera_type_entry = Entry(main, style="SELF.TEntry")
        self.camera_type_entry.grid(row=3, column=1, padx=[0, 10], pady=[5, 10], sticky=W + E)

        # Frames tab content.
        frames = Frame(notebook)
        frames.columnconfigure(1, weight=1)

        frame_interval_label = Label(frames, text="Frame interval", style="SELF.TLabel")
        frame_interval_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.frame_interval_entry = Entry(frames, style="SELF.TEntry")
        self.frame_interval_entry.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        frame_rate_label = Label(frames, text="Frame rate", style="SELF.TLabel")
        frame_rate_label.grid(row=1, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.frame_rate_entry = Entry(frames, style="SELF.TEntry")
        self.frame_rate_entry.grid(row=1, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        frame_count_label = Label(frames, text="Frame count", style="SELF.TLabel")
        frame_count_label.grid(row=2, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.frame_count_entry = Entry(frames, style="SELF.TEntry")
        self.frame_count_entry.grid(row=2, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        # Cameras tab content.
        cameras = Frame(notebook)
        cameras.columnconfigure(1, weight=1)

        cam_0_label = Label(cameras, text="Camera 0", style="SELF.TLabel")
        cam_0_label.grid(row=0, column=0, padx=[10, 0], pady=[10, 0], sticky=W)
        self.cam_0_entry = Entry(cameras, style="SELF.TEntry")
        self.cam_0_entry.grid(row=0, column=1, padx=[0, 10], pady=[10, 0], sticky=W + E)

        cam_1_label = Label(cameras, text="Camera 1", style="SELF.TLabel")
        cam_1_label.grid(row=1, column=0, padx=[10, 0], pady=[5, 0], sticky=W)
        self.cam_1_entry = Entry(cameras, style="SELF.TEntry")
        self.cam_1_entry.grid(row=1, column=1, padx=[0, 10], pady=[5, 0], sticky=W + E)

        cam_2_label = Label(cameras, text="Camera 2", style="SELF.TLabel")
        cam_2_label.grid(row=2, column=0, padx=[10, 0], pady=[5, 0], sticky=W)
        self.cam_2_entry = Entry(cameras, style="SELF.TEntry")
        self.cam_2_entry.grid(row=2, column=1, padx=[0, 10], pady=[5, 0], sticky=W + E)

        cam_3_type_label = Label(cameras, text="Camera 3", style="SELF.TLabel")
        cam_3_type_label.grid(row=3, column=0, padx=[10, 0], pady=[5, 10], sticky=W)
        self.cam_3_entry = Entry(cameras, style="SELF.TEntry")
        self.cam_3_entry.grid(row=3, column=1, padx=[0, 10], pady=[5, 10], sticky=W + E)

        # Add the tabs.
        notebook.add(main, text="Main")
        notebook.add(frames, text="Frames")
        notebook.add(cameras, text="Cameras")

        notebook.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=W + E)

        accept_button = Button(self, text="Accept")
        accept_button.grid(row=1, column=1, padx=[0, 10], sticky=N + E)
        accept_button.bind("<Button-1>", self.on_accept_button_click)

        default_button = Button(self, text="Default")
        default_button.grid(row=1, column=2, padx=[0, 10], sticky=N + E)
        default_button.bind("<Button-1>", self.on_default_button_click)

        cancel_button = Button(self, text="Cancel")
        cancel_button.grid(row=1, column=3, padx=[0, 10], sticky=N + E)
        cancel_button.bind("<Button-1>", self.on_cancel_button_click)

        # Load configuration.
        self.load_config()

    def on_accept_button_click(self, _):
        self.save_config()

    def on_default_button_click(self, _):
        res = messagebox.askyesno("Confirm Settings Reset", "Are you sure you want to reset settings to default?")

        if res is True:
            reset_default()
            self.reset_form()
            self.load_config()

    def on_cancel_button_click(self, _):
        self.master.destroy()

    def reset_form(self):
        """Clear the current form content"""
        self.screen_entry.delete(0, END)
        self.width_entry.delete(0, END)
        self.height_entry.delete(0, END)
        self.camera_type_entry.delete(0, END)
        self.frame_interval_entry.delete(0, END)
        self.frame_rate_entry.delete(0, END)
        self.frame_count_entry.delete(0, END)
        self.cam_0_entry.delete(0, END)
        self.cam_1_entry.delete(0, END)
        self.cam_2_entry.delete(0, END)
        self.cam_3_entry.delete(0, END)

    def load_config(self):
        data = read_settings()

        # Load main section.
        self.screen_entry.insert(0, data["main"]["screen"])
        self.width_entry.insert(0, data["main"]["width_percent"])
        self.height_entry.insert(0, data["main"]["height_percent"])
        self.camera_type_entry.insert(0, data["main"]["type_camera"])

        # Load frames section
        self.frame_interval_entry.insert(0, data["frames"]["frame_interval"])
        self.frame_rate_entry.insert(0, data["frames"]["frame_rate"])
        self.frame_count_entry.insert(0, data["frames"]["frame_count"])

        # Load cameras section
        self.cam_0_entry.insert(0, data["cameras"]["0"])
        self.cam_1_entry.insert(0, data["cameras"]["1"])
        self.cam_2_entry.insert(0, data["cameras"]["2"])
        self.cam_3_entry.insert(0, data["cameras"]["3"])

        # Set the class data field to the JSON dict.
        self.data = data

    def save_config(self):
        data = self.data

        # Set main section.
        data["main"]["screen"] = self.screen_entry.get()
        data["main"]["width_percent"] = self.width_entry.get()
        data["main"]["height_percent"] = self.height_entry.get()
        data["main"]["type_camera"] = self.camera_type_entry.get()

        # Set frames section.
        data["frames"]["frame_interval"] = self.frame_interval_entry.get()
        data["frames"]["frame_rate"] = self.frame_rate_entry.get()
        data["frames"]["frame_count"] = self.frame_count_entry.get()

        # Set cameras section.
        data["cameras"]["0"] = self.cam_0_entry.get()
        data["cameras"]["1"] = self.cam_1_entry.get()
        data["cameras"]["2"] = self.cam_2_entry.get()
        data["cameras"]["3"] = self.cam_3_entry.get()

        # Save JSON data into file.
        if not write_settings(data):
            messagebox.showerror(title="An Error Occurred!", message="Couldn't save the changes.")
        else:
            self.master.destroy()
