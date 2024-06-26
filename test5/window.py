import tkinter as tk
from APIcall import APIcall

class BaseWindow:
    def __init__(self, title, width, height):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

    def run(self):
        self.root.mainloop()

class SubPage(tk.Frame):
    def __init__(self, master, title, messages, text_font_size, navigate_home):
        super().__init__(master)
        self.title = title
        self.messages = messages
        self.text_font_size = text_font_size
        self.navigate_home = navigate_home
        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, anchor='nw', pady=10, padx=10)

        home_button = tk.Button(button_frame, text="Return to Main", command=self.navigate_home)
        home_button.pack(side=tk.LEFT, padx=5)

        label = tk.Label(self, text=self.title, font=("Times New Roman", self.text_font_size, "bold"))
        label.pack(pady=20)

        icon_frame = tk.Frame(self)
        icon_frame.pack(expand=True, fill=tk.BOTH)

        grid_size = (3, 2) if len(self.messages) == 6 else (4, 3)
        for index, (message, callback) in enumerate(self.messages):
            button = tk.Button(icon_frame, text=message, wraplength=100, font=("Times New Roman", self.text_font_size), command=callback)
            row, col = divmod(index, grid_size[0])
            button.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        # Configure grid weights to evenly distribute space
        for row in range(grid_size[1]):
            icon_frame.grid_rowconfigure(row, weight=1)
        for col in range(grid_size[0]):
            icon_frame.grid_columnconfigure(col, weight=1)

class SecondLevelSubPage(tk.Frame):
    def __init__(self, master, title, topic, content, topic_font_size, content_font_size, navigate_back, navigate_home):
        super().__init__(master)
        self.title = title
        self.topic = topic
        self.content = content
        self.topic_font_size = topic_font_size
        self.content_font_size = content_font_size
        self.navigate_back = navigate_back
        self.navigate_home = navigate_home
        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, anchor='nw', pady=10, padx=10)

        back_button = tk.Button(button_frame, text="Return to Previous", command=self.navigate_back)
        back_button.pack(side=tk.LEFT, padx=5)

        home_button = tk.Button(button_frame, text="Return to Main", command=self.navigate_home)
        home_button.pack(side=tk.LEFT, padx=5)

        topic_label = tk.Label(self, text=self.topic, font=("Times New Roman", self.topic_font_size))
        topic_label.pack(pady=10)

        # Frame for the content
        content_frame = tk.Frame(self)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=20, pady=10)

        content_text = tk.Text(content_frame, wrap=tk.WORD, font=("Times New Roman", self.content_font_size), height=4)
        content_text.insert(tk.END, self.content)
        content_text.config(state=tk.DISABLED)
        content_text.pack(expand=False, fill=tk.BOTH)

        # Frame for API call section
        api_frame = tk.Frame(self)
        api_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Integrate APIcall functionality
        self.api_call = APIcall(api_frame)
