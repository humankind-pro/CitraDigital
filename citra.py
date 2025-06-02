import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("1000x700") # Sedikit menambah tinggi window

        self.original_image = None
        self.processed_image = None
        self.current_image_path = None # Untuk menyimpan path gambar asli

        self.create_widgets()

    def create_widgets(self):
        # Frame tombol
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=10)

        # --- Tombol Operasi Dasar ---
        basic_op_frame = tk.LabelFrame(controls_frame, text="Operasi Dasar")
        basic_op_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

        tk.Button(basic_op_frame, text="Buka Gambar", command=self.load_image, width=20).pack(pady=5, padx=5)
        tk.Button(basic_op_frame, text="Simpan Gambar Hasil", command=self.save_processed_image, width=20).pack(pady=5, padx=5)
        tk.Button(basic_op_frame, text="Reset Gambar", command=self.reset_image, width=20).pack(pady=5, padx=5)


        # --- Tombol Pemrosesan Gambar ---
        processing_op_frame = tk.LabelFrame(controls_frame, text="Pemrosesan Citra")
        processing_op_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ns")

        tk.Button(processing_op_frame, text="Grayscale", command=self.convert_to_grayscale, width=20).pack(pady=5, padx=5)
        tk.Button(processing_op_frame, text="Citra Biner", command=self.convert_to_binary, width=20).pack(pady=5, padx=5)
        tk.Button(processing_op_frame, text="Tambah Kecerahan (Add)", command=self.arithmetic_addition, width=20).pack(pady=5, padx=5)
        tk.Button(processing_op_frame, text="Inversi Warna (NOT)", command=self.logic_not_operation, width=20).pack(pady=5, padx=5)


        # Frame tampilan gambar
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.original_panel = tk.Label(self.image_frame) # Mengganti nama variabel untuk konsistensi
        self.original_panel.pack(side="left", padx=10, fill="both", expand=True)

        self.processed_panel = tk.Label(self.image_frame) # Mengganti nama variabel untuk konsistensi
        self.processed_panel.pack(side="right", padx=10, fill="both", expand=True)

        # Label untuk panel gambar
        original_label_text = tk.Label(self.image_frame, text="Gambar Asli")
        processed_label_text = tk.Label(self.image_frame, text="Gambar Hasil Proses")

        # Tempatkan label di atas panel yang sesuai
        # Ini adalah cara sederhana, bisa disempurnakan dengan grid jika tata letak lebih kompleks
        original_label_text.place(in_=self.original_panel, relx=0.5, rely=-0.05, anchor="n") # Disesuaikan
        processed_label_text.place(in_=self.processed_panel, relx=0.5, rely=-0.05, anchor="n") # Disesuaikan


    def _check_image_loaded(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Tidak ada gambar yang dimuat. Silakan buka gambar terlebih dahulu.")
            return False
        return True

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
        if not path:
            return
        self.current_image_path = path
        self.original_image = cv2.imread(path)
        if self.original_image is None:
            messagebox.showerror("Error Memuat Gambar", f"Tidak dapat memuat gambar dari: {path}")
            return
        self.display_image(self.original_image, self.original_panel, "Gambar Asli")
        # Saat gambar baru dimuat, bersihkan panel gambar yang diproses
        self.processed_image = None
        self.processed_panel.config(image='', text="Gambar Hasil Proses")
        self.processed_panel.image = None


    def display_image(self, image_cv, panel, title_prefix=""):
        if image_cv is None:
            panel.config(image='', text=f"{title_prefix}\n(Kosong)")
            panel.image = None
            return

        # Resize image agar sesuai dengan panel, jaga aspek rasio
        panel_width = self.image_frame.winfo_width() // 2 - 20 # perkiraan lebar panel
        panel_height = self.image_frame.winfo_height() - 40 # perkiraan tinggi panel
        if panel_width <=0 : panel_width = 400 # default jika window belum digambar
        if panel_height <=0 : panel_height = 300 # default

        h, w = image_cv.shape[:2]
        aspect_ratio = w / h

        if w > panel_width or h > panel_height:
            if w / panel_width > h / panel_height:
                new_w = panel_width
                new_h = int(new_w / aspect_ratio)
            else:
                new_h = panel_height
                new_w = int(new_h * aspect_ratio)
        else:
            new_w, new_h = w, h
        
        resized_image_cv = cv2.resize(image_cv, (new_w, new_h), interpolation=cv2.INTER_AREA)

        # Konversi ke format yang bisa ditampilkan Tkinter
        if len(resized_image_cv.shape) == 2: # Grayscale
            image_rgb = cv2.cvtColor(resized_image_cv, cv2.COLOR_GRAY2RGB)
        else: # Berwarna (BGR)
            image_rgb = cv2.cvtColor(resized_image_cv, cv2.COLOR_BGR2RGB)
        
        image_pil = Image.fromarray(image_rgb)
        photo = ImageTk.PhotoImage(image_pil)

        panel.image = photo # Simpan referensi agar tidak di-garbage collect
        panel.config(image=photo, text="") # Hapus teks jika gambar ada

    def reset_image(self):
        if self.current_image_path:
            self.original_image = cv2.imread(self.current_image_path)
            self.display_image(self.original_image, self.original_panel, "Gambar Asli")
            self.processed_image = None
            self.processed_panel.config(image='', text="Gambar Hasil Proses")
            self.processed_panel.image = None
            messagebox.showinfo("Reset", "Gambar telah dikembalikan ke kondisi asli.")
        else:
            messagebox.showwarning("Reset", "Tidak ada gambar asli untuk di-reset.")

    def save_processed_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "Tidak ada gambar hasil proses untuk disimpan.")
            return

        path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"),
                                                          ("JPEG files", "*.jpg;*.jpeg"),
                                                          ("BMP files", "*.bmp"),
                                                          ("All files", "*.*")])
        if not path:
            return

        try:
            # PIL/Pillow menangani gambar RGB, OpenCV menangani BGR.
            # Jika self.processed_image adalah BGR (umumnya dari cv2), simpan langsung.
            # Jika self.processed_image adalah format lain (misal sudah diubah ke RGB untuk display),
            # pastikan konversi yang benar sebelum menyimpan.
            # Untuk konsistensi, kita asumsikan self.processed_image selalu dalam format BGR (OpenCV default)
            # atau grayscale. cv2.imwrite bisa menangani keduanya.
            cv2.imwrite(path, self.processed_image)
            messagebox.showinfo("Sukses", f"Gambar berhasil disimpan di: {path}")
        except Exception as e:
            messagebox.showerror("Error Menyimpan", f"Terjadi kesalahan: {e}")

    # --- METODE PEMROSESAN GAMBAR ---
    def convert_to_grayscale(self):
        if not self._check_image_loaded():
            return
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # Simpan sebagai gambar grayscale (1 channel) tapi untuk display kita bisa buat 3 channel
        self.processed_image = gray_image # Simpan versi grayscale asli
        # Untuk display yang konsisten, kita bisa kirim versi yang bisa langsung di-render display_image
        displayable_gray = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
        self.display_image(displayable_gray, self.processed_panel, "Hasil Grayscale")

    def convert_to_binary(self):
        if not self._check_image_loaded():
            return
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # Tentukan threshold, bisa menggunakan Otsu atau nilai tetap
        # Di sini kita pakai nilai tetap 127 untuk contoh
        _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        self.processed_image = binary_image # Simpan versi biner asli (1 channel)
        displayable_binary = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)
        self.display_image(displayable_binary, self.processed_panel, "Hasil Biner")

    def arithmetic_addition(self):
        if not self._check_image_loaded():
            return
        
        # Minta input nilai penambah kecerahan dari pengguna
        value_str = simpledialog.askstring("Input Kecerahan", "Masukkan nilai penambah kecerahan (misal: 50):",
                                           parent=self.root)
        if value_str is None: # Pengguna membatalkan dialog
            return
            
        try:
            value = int(value_str)
        except ValueError:
            messagebox.showerror("Input Tidak Valid", "Harap masukkan angka yang valid.")
            return

        # Pastikan original_image adalah BGR 3 channel
        if len(self.original_image.shape) == 2: # Jika gambar asli adalah grayscale
            # Buat matriks dengan nilai yang sama untuk semua channel (jika perlu)
            # atau operasikan langsung pada grayscale
             M = np.ones(self.original_image.shape, dtype="uint8") * value
             added_image = cv2.add(self.original_image, M)
        elif len(self.original_image.shape) == 3 and self.original_image.shape[2] == 3: # BGR
            M = np.ones(self.original_image.shape, dtype="uint8") * value
            added_image = cv2.add(self.original_image, M)
            # Alternatif: added_image = np.clip(self.original_image.astype(np.int16) + value, 0, 255).astype(np.uint8)
        else:
            messagebox.showerror("Error", "Format gambar input tidak didukung untuk operasi ini.")
            return

        self.processed_image = added_image
        self.display_image(self.processed_image, self.processed_panel, f"Hasil Kecerahan +{value}")


    def logic_not_operation(self):
        if not self._check_image_loaded():
            return
        inverted_image = cv2.bitwise_not(self.original_image)
        self.processed_image = inverted_image
        self.display_image(self.processed_image, self.processed_panel, "Hasil Inversi (NOT)")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()