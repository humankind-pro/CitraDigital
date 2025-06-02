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

        tk.Button(button_frame, text="Buka Gambar").grid(row=0, column=0, padx=5)


        # Frame tampilan gambar
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10)

        self.original_label = tk.Label(self.image_frame, text="Gambar Asli")
        self.original_label.grid(row=0, column=0)

        self.processed_label = tk.Label(self.image_frame, text="Gambar Hasil")
        self.processed_label.grid(row=0, column=1)

        self.original_canvas = tk.Label(self.image_frame)
        self.original_canvas.grid(row=1, column=0)

        self.processed_canvas = tk.Label(self.image_frame)
        self.processed_canvas.grid(row=1, column=1)

    



if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
