import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("1000x600")

        self.original_image = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        # Frame tombol
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Buka Gambar", command=self.load_image).grid(row=0, column=0, padx=5)


        # Frame tampilan gambar
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10)

        self.original_label = tk.Label(self.image_frame, text="Gambar Asli")
        self.original_label.grid(row=0, column=0)


        self.original_canvas = tk.Label(self.image_frame)
        self.original_canvas.grid(row=1, column=0)

        self.processed_canvas = tk.Label(self.image_frame)
        self.processed_canvas.grid(row=1, column=1)

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        self.original_image = cv2.imread(path)
        self.display_image(self.original_image, self.original_canvas)

    def display_image(self, image, canvas):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_pil = image_pil.resize((400, 300))
        photo = ImageTk.PhotoImage(image_pil)
        canvas.image = photo
        canvas.config(image=photo)



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
