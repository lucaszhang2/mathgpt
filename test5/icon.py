from PIL import Image, ImageTk
import tkinter as tk

class Icon:
    def __init__(self, name, path, title, message):
        self.name = name
        self.path = path
        self.title = title
        self.message = message

    def create_button(self, master, callback):
        # Load the image
        self.original_img = Image.open(self.path)
        self.img = ImageTk.PhotoImage(self.original_img)

        # Create the button with minimal padding and border
        button = tk.Button(
            master,
            image=self.img,
            text=self.name,
            compound=tk.TOP,
            command=lambda: callback(self.title, self.message),
            borderwidth=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            wraplength=100  # Adjust the wrap length as needed
        )
        button.image = self.img  # Keep a reference to avoid garbage collection

        # Bind the <Configure> event to dynamically resize the image
        button.bind('<Configure>', self.resize_image)

        return button

    def resize_image(self, event):
        # Resize the image to fit the button dimensions
        new_width = event.width
        new_height = int(event.height * 0.6)
        resized_img = self.original_img.resize((new_width, new_height), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized_img)

        # Update the button's image
        event.widget.config(image=self.img)
        event.widget.image = self.img  # Keep a reference to avoid garbage collection
