import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')

        self.original_image = None
        self.processed_image = None
        self.current_image_path = None
        self.second_image = None

        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        controls_frame = tk.Frame(main_frame, bg='#f0f0f0')
        controls_frame.pack(pady=10)

        basic_op_frame = tk.LabelFrame(controls_frame, text="Operasi Dasar", font=('Arial', 10, 'bold'), bg='#f0f0f0')
        basic_op_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

        self.btn_load = tk.Button(basic_op_frame, text="Buka Gambar", command=self.load_image, width=22, bg='#4CAF50', fg='white', font=('Arial', 9))
        self.btn_load.grid(row=0, column=0, pady=5, padx=5)
        self.btn_load_second = tk.Button(basic_op_frame, text="Buka Gambar Kedua", command=self.load_second_image, width=22, bg='#2196F3', fg='white', font=('Arial', 9))
        self.btn_load_second.grid(row=1, column=0, pady=5, padx=5)
        self.btn_save = tk.Button(basic_op_frame, text="Simpan Gambar Hasil", command=self.save_processed_image, width=22, bg='#FF9800', fg='white', font=('Arial', 9))
        self.btn_save.grid(row=2, column=0, pady=5, padx=5)
        self.btn_reset = tk.Button(basic_op_frame, text="Reset Gambar", command=self.reset_image, width=22, bg='#f44336', fg='white', font=('Arial', 9))
        self.btn_reset.grid(row=3, column=0, pady=5, padx=5)

        processing_op_frame = tk.LabelFrame(controls_frame, text="Pemrosesan Citra", 
                                          font=('Arial', 10, 'bold'), bg='#f0f0f0')
        processing_op_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ns")
        
        tk.Button(processing_op_frame, text="Grayscale", command=self.convert_to_grayscale, 
                 width=22, bg='#9C27B0', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(processing_op_frame, text="Citra Biner", command=self.convert_to_binary, 
                 width=22, bg='#607D8B', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(processing_op_frame, text="Tambah Kecerahan", command=self.arithmetic_addition, 
                 width=22, bg='#795548', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(processing_op_frame, text="Kurangi Kecerahan", command=self.arithmetic_subtraction, 
                 width=22, bg='#3F51B5', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(processing_op_frame, text="Erosi", command=self.morphological_erosion, 
                 width=22, bg='#FF9800', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(processing_op_frame, text="Tampilkan Histogram", command=self.show_histogram, 
                 width=22, bg='#FF5722', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)

        logic_op_frame = tk.LabelFrame(controls_frame, text="Operasi Logika", font=('Arial', 10, 'bold'), bg='#f0f0f0')
        logic_op_frame.grid(row=0, column=2, padx=10, pady=5, sticky="ns")

        self.btn_not = tk.Button(logic_op_frame, text="Inversi (NOT)", command=self.logic_not_operation, width=22, bg='#E91E63', fg='white', font=('Arial', 9))
        self.btn_not.grid(row=0, column=0, pady=3, padx=5)
        self.btn_and = tk.Button(logic_op_frame, text="AND (Dua Gambar)", command=self.logic_and_operation, width=22, bg='#009688', fg='white', font=('Arial', 9))
        self.btn_and.grid(row=1, column=0, pady=3, padx=5)
        self.btn_or = tk.Button(logic_op_frame, text="OR (Dua Gambar)", command=self.logic_or_operation, width=22, bg='#FF5722', fg='white', font=('Arial', 9))
        self.btn_or.grid(row=2, column=0, pady=3, padx=5)
        self.btn_xor = tk.Button(logic_op_frame, text="XOR (Dua Gambar)", command=self.logic_xor_operation, width=22, bg='#673AB7', fg='white', font=('Arial', 9))
        self.btn_xor.grid(row=3, column=0, pady=3, padx=5)

        # --- Tombol Filter ---
        filter_op_frame = tk.LabelFrame(controls_frame, text="Filter & Efek", 
                                      font=('Arial', 10, 'bold'), bg='#f0f0f0')
        filter_op_frame.grid(row=0, column=3, padx=10, pady=5, sticky="ns")

        tk.Button(filter_op_frame, text="Blur", command=self.apply_blur, 
                 width=22, bg='#8BC34A', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(filter_op_frame, text="Sharpen", command=self.apply_sharpen, 
                 width=22, bg='#CDDC39', fg='black', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(filter_op_frame, text="Edge Detection", command=self.edge_detection, 
                 width=22, bg='#FFC107', fg='black', font=('Arial', 9)).pack(pady=3, padx=5)
        tk.Button(filter_op_frame, text="Histogram Equalization", command=self.histogram_equalization, 
                 width=22, bg='#FF9800', fg='white', font=('Arial', 9)).pack(pady=3, padx=5)

        self.image_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.image_frame.pack(pady=10, padx=10, fill="both", expand=True)

        original_frame = tk.LabelFrame(self.image_frame, text="Gambar Asli", font=('Arial', 10, 'bold'), bg='white')
        original_frame.pack(side="left", padx=10, fill="both", expand=True)
        self.original_panel = tk.Label(original_frame, text="Klik 'Buka Gambar' untuk memulai", bg='white', fg='gray', font=('Arial', 12))
        self.original_panel.pack(padx=10, pady=10, fill="both", expand=True)

        processed_frame = tk.LabelFrame(self.image_frame, text="Gambar Hasil Proses", font=('Arial', 10, 'bold'), bg='white')
        processed_frame.pack(side="right", padx=10, fill="both", expand=True)
        self.processed_panel = tk.Label(processed_frame, text="Hasil pemrosesan akan muncul di sini", bg='white', fg='gray', font=('Arial', 12))
        self.processed_panel.pack(padx=10, pady=10, fill="both", expand=True)

        self.status_var = tk.StringVar()
        self.status_var.set("Siap")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, bg='#e0e0e0')
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.image_frame.bind("<Configure>", lambda e: self._update_displayed_images())

    def update_status(self, message):
        self.status_var.set(message)
        self.root.update_idletasks()

    def _check_image_loaded(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Tidak ada gambar yang dimuat. Silakan buka gambar terlebih dahulu.")
            return False
        return True

    def _check_two_images_loaded(self):
        if self.original_image is None or self.second_image is None:
            messagebox.showerror("Error", "Diperlukan dua gambar untuk operasi ini. Pastikan gambar asli dan gambar kedua sudah dimuat.")
            return False
        if self.original_image.shape != self.second_image.shape:
            messagebox.showerror("Error", "Ukuran atau jumlah channel gambar asli dan gambar kedua harus sama.")
            return False
        return True

    def _load_image_with_pil_fallback(self, path):
        try:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if img is None:
                pil_img = Image.open(path)
                if pil_img.mode == 'RGBA':
                    pil_img = pil_img.convert('RGB')
                elif pil_img.mode != 'RGB':
                    pil_img = pil_img.convert('RGB')
                img = np.array(pil_img)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if len(img.shape) == 3 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
        except Exception as e:
            raise ValueError(f"Tidak dapat memuat gambar dari: {os.path.basename(path)}. Error: {str(e)}")

    def load_image(self):
        file_types = [
            ("All files", "*.*"),
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.heic")
        ]
        path = filedialog.askopenfilename(filetypes=file_types)
        if not path:
            return
        try:
            self.current_image_path = path
            self.original_image = self._load_image_with_pil_fallback(path)
            self.display_image(self.original_image, self.original_panel)
            self.processed_image = None
            self.processed_panel.config(image='', text="Hasil pemrosesan akan muncul di sini")
            self.processed_panel.image = None
            self.update_status(f"Gambar dimuat: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat gambar: {str(e)}")
            self.update_status("Gagal memuat gambar.")

    def load_second_image(self):
        if not self._check_image_loaded():
            return
        file_types = [
            ("All files", "*.*"),
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.heic")
        ]
        path = filedialog.askopenfilename(filetypes=file_types)
        if not path:
            return
        try:
            second_img = self._load_image_with_pil_fallback(path)
            h, w = self.original_image.shape[:2]
            second_img = cv2.resize(second_img, (w, h), interpolation=cv2.INTER_AREA)
            if len(self.original_image.shape) == 3 and len(second_img.shape) == 2:
                second_img = cv2.cvtColor(second_img, cv2.COLOR_GRAY2BGR)
            elif len(self.original_image.shape) == 2 and len(second_img.shape) == 3:
                second_img = cv2.cvtColor(second_img, cv2.COLOR_BGR2GRAY)
            self.second_image = second_img
            self.update_status(f"Gambar kedua dimuat: {os.path.basename(path)}")
            messagebox.showinfo("Sukses", "Gambar kedua berhasil dimuat untuk operasi logika.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat gambar kedua: {str(e)}")
            self.update_status("Gagal memuat gambar kedua.")

    def display_image(self, image_cv, panel):
        if image_cv is None:
            panel.config(image='', text="Tidak ada gambar")
            panel.image = None
            return
        try:
            panel_width = self.image_frame.winfo_width() // 2 - 20 or 400
            panel_height = self.image_frame.winfo_height() - 40 or 300
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
            if len(resized_image_cv.shape) == 2:
                image_rgb = cv2.cvtColor(resized_image_cv, cv2.COLOR_GRAY2RGB)
            else:
                image_rgb = cv2.cvtColor(resized_image_cv, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            photo = ImageTk.PhotoImage(image_pil)
            panel.image = photo
            panel.config(image=photo, text="")
        except Exception as e:
            panel.config(image='', text=f"Error menampilkan gambar: {str(e)}")
            panel.image = None
            self.update_status("Gagal menampilkan gambar.")

    def _update_displayed_images(self):
        if self.original_image is not None:
            self.display_image(self.original_image, self.original_panel)
        if self.processed_image is not None:
            self.display_image(self.processed_image, self.processed_panel)

    def reset_image(self):
        if not self.current_image_path:
            messagebox.showwarning("Reset", "Tidak ada gambar asli untuk di-reset.")
            return
        try:
            self.original_image = self._load_image_with_pil_fallback(self.current_image_path)
            self.display_image(self.original_image, self.original_panel)
            self.processed_image = None
            self.second_image = None
            self.processed_panel.config(image='', text="Hasil pemrosesan akan muncul di sini")
            self.processed_panel.image = None
            self.update_status("Gambar di-reset ke kondisi asli")
            messagebox.showinfo("Reset", "Gambar telah dikembalikan ke kondisi asli.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal me-reset gambar: {str(e)}")
            self.update_status("Gagal me-reset gambar.")

    def save_processed_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "Tidak ada gambar hasil proses untuk disimpan.")
            return
        file_types = [
            ("All files", "*.*"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff"),
            ("WebP files", "*.webp")
        ]
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=file_types)
        if not path:
            return
        try:
            save_img = self.processed_image
            if len(save_img.shape) == 2 and path.lower().endswith(('.jpg', '.jpeg', '.webp')):
                save_img = cv2.cvtColor(save_img, cv2.COLOR_GRAY2BGR)
            cv2.imwrite(path, save_img)
            self.update_status(f"Gambar disimpan: {os.path.basename(path)}")
            messagebox.showinfo("Sukses", f"Gambar berhasil disimpan di: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat menyimpan: {str(e)}")
            self.update_status("Gagal menyimpan gambar.")

    def convert_to_grayscale(self):
        if not self._check_image_loaded():
            return
        try:
            if len(self.original_image.shape) == 3:
                gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = self.original_image
            self.processed_image = gray_image
            self.display_image(gray_image, self.processed_panel)
            self.update_status("Konversi ke grayscale selesai")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengkonversi ke grayscale: {str(e)}")
            self.update_status("Gagal mengkonversi ke grayscale.")

    def convert_to_binary(self):
        if not self._check_image_loaded():
            return
        try:
            threshold_str = simpledialog.askstring("Input Threshold", "Masukkan nilai threshold (0-255, default: 127):", parent=self.root)
            threshold = 127
            if threshold_str:
                try:
                    threshold = int(threshold_str)
                    threshold = max(0, min(255, threshold))
                except ValueError:
                    messagebox.showwarning("Input", "Nilai tidak valid, menggunakan threshold default (127)")
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY) if len(self.original_image.shape) == 3 else self.original_image
            _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
            self.processed_image = binary_image
            self.display_image(binary_image, self.processed_panel)
            self.update_status(f"Konversi ke biner selesai (threshold: {threshold})")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengkonversi ke biner: {str(e)}")
            self.update_status("Gagal mengkonversi ke biner.")

    def morphological_erosion(self):
        if not self._check_image_loaded():
            return
        try:
            # Definisikan elemen penstruktur (SE)
            se1 = np.array([[1, 1, 1],
                            [1, 1, 1],
                            [1, 1, 1]], dtype=np.uint8)  # SE 1: Persegi 3x3
            se2 = np.array([[0, 1, 0],
                            [1, 1, 1],
                            [0, 1, 0]], dtype=np.uint8)  # SE 2: Disk radius 1
            
            # Lakukan erosi dengan kedua elemen penstruktur
            eroded_image1 = cv2.erode(self.original_image, se1)
            eroded_image2 = cv2.erode(self.original_image, se2)
            # Gabungkan hasil erosi
            self.processed_image = cv2.bitwise_or(eroded_image1, eroded_image2)
            # Tampilkan gambar hasil
            self.display_image(self.processed_image, self.processed_panel)
            self.update_status("Operasi erosi selesai")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan operasi erosi: {str(e)}")

        # Tambahkan metode show_histogram di sini
    def show_histogram(self):
        """Tampilkan histogram dari gambar asli"""
        if not self._check_image_loaded():
            return
        try:
            # Hitung histogram untuk setiap channel (B, G, R)
            colors = ('b', 'g', 'r')
            plt.figure(figsize=(10, 5))
            for i, color in enumerate(colors):
                hist = cv2.calcHist([self.original_image], [i], None, [256], [0, 256])
                plt.plot(hist, color=color)
                plt.xlim([0, 256])
            plt.title('Histogram Gambar')
            plt.xlabel('Intensitas Pixel')
            plt.ylabel('Jumlah Pixel')
            plt.legend(['B', 'G', 'R'])
            plt.show()
            self.update_status("Histogram ditampilkan")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan histogram: {str(e)}")

    def arithmetic_addition(self):
        if not self._check_image_loaded():
            return
        try:
            value_str = simpledialog.askstring("Input Kecerahan", "Masukkan nilai penambah kecerahan (0-100, default: 50):", parent=self.root)
            value = 50
            if value_str:
                try:
                    value = int(value_str)
                    value = max(0, min(100, value))
                except ValueError:
                    messagebox.showwarning("Input", "Nilai tidak valid, menggunakan nilai default (50)")
            M = np.ones(self.original_image.shape, dtype="uint8") * value
            added_image = cv2.add(self.original_image, M)
            self.processed_image = added_image
            self.display_image(added_image, self.processed_panel)
            self.update_status(f"Kecerahan ditambah: +{value}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah kecerahan: {str(e)}")
            self.update_status("Gagal menambah kecerahan.")

    def arithmetic_subtraction(self):
        if not self._check_image_loaded():
            return
        try:
            value_str = simpledialog.askstring("Input Kecerahan", "Masukkan nilai pengurang kecerahan (0-100, default: 50):", parent=self.root)
            value = 50
            if value_str:
                try:
                    value = int(value_str)
                    value = max(0, min(100, value))
                except ValueError:
                    messagebox.showwarning("Input", "Nilai tidak valid, menggunakan nilai default (50)")
            M = np.ones(self.original_image.shape, dtype="uint8") * value
            subtracted_image = cv2.subtract(self.original_image, M)
            self.processed_image = subtracted_image
            self.display_image(subtracted_image, self.processed_panel)
            self.update_status(f"Kecerahan dikurangi: -{value}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengurangi kecerahan: {str(e)}")
            self.update_status("Gagal mengurangi kecerahan.")

    def logic_not_operation(self):
        if not self._check_image_loaded():
            return
        try:
            inverted_image = cv2.bitwise_not(self.original_image)
            self.processed_image = inverted_image
            self.display_image(inverted_image, self.processed_panel)
            self.update_status("Operasi NOT (inversi) selesai")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan operasi NOT: {str(e)}")
            self.update_status("Gagal melakukan operasi NOT.")

    def logic_and_operation(self):
        if not self._check_two_images_loaded():
            return
        try:
            and_result = cv2.bitwise_and(self.original_image, self.second_image)
            self.processed_image = and_result
            self.display_image(and_result, self.processed_panel)
            self.update_status("Operasi AND selesai")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan operasi AND: {str(e)}")
            self.update_status("Gagal melakukan operasi AND.")

    def logic_or_operation(self):
        if not self._check_two_images_loaded():
            return
        try:
            or_result = cv2.bitwise_or(self.original_image, self.second_image)
            self.processed_image = or_result
            self.display_image(or_result, self.processed_panel)
            self.update_status("Operasi OR selesai")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan operasi OR: {str(e)}")
            self.update_status("Gagal melakukan operasi OR.")

    def logic_xor_operation(self):
        if not self._check_two_images_loaded():
            return
        try:
            xor_result = cv2.bitwise_xor(self.original_image, self.second_image)
            self.processed_image = xor_result
            self.display_image(xor_result, self.processed_panel)
            self.update_status("Operasi XOR selesai")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan operasi XOR: {str(e)}")
            self.update_status("Gagal melakukan operasi XOR.")

    def on_closing(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
            self.root.destroy()

   # === FILTER DAN EFEK TAMBAHAN ===

    def apply_blur(self):
        """Aplikasikan filter blur"""
        if not self._check_image_loaded():
            return
        
        try:
            kernel_str = simpledialog.askstring(
                "Input Kernel Size", 
                "Masukkan ukuran kernel blur (5, 15, 25, default: 15):",
                parent=self.root
            )
            
            if kernel_str is None:
                return
                
            try:
                kernel_size = int(kernel_str) if kernel_str else 15
                # Pastikan kernel size ganjil dan positif
                kernel_size = max(3, kernel_size)
                if kernel_size % 2 == 0:
                    kernel_size += 1
            except ValueError:
                kernel_size = 15

            blurred_image = cv2.GaussianBlur(self.original_image, (kernel_size, kernel_size), 0)
            self.processed_image = blurred_image
            self.display_image(self.processed_image, self.processed_panel)
            
            self.update_status(f"Filter blur diterapkan (kernel: {kernel_size}x{kernel_size})")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menerapkan blur: {str(e)}")

    def apply_sharpen(self):
        """Aplikasikan filter sharpen"""
        if not self._check_image_loaded():
            return
        
        try:
            # Kernel untuk sharpening
            kernel = np.array([[-1,-1,-1],
                             [-1, 9,-1],
                             [-1,-1,-1]])
            
            sharpened_image = cv2.filter2D(self.original_image, -1, kernel)
            self.processed_image = sharpened_image
            self.display_image(self.processed_image, self.processed_panel)
            
            self.update_status("Filter sharpen diterapkan")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menerapkan sharpen: {str(e)}")

    def edge_detection(self):
        """Deteksi tepi menggunakan Canny"""
        if not self._check_image_loaded():
            return
        
        try:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            
            # Konversi ke BGR untuk konsistensi
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            self.processed_image = edges_bgr
            self.display_image(self.processed_image, self.processed_panel)
            
            self.update_status("Deteksi tepi (Canny) selesai")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan deteksi tepi: {str(e)}")

    def histogram_equalization(self):
        """Histogram equalization untuk peningkatan kontras"""
        if not self._check_image_loaded():
            return
        
        try:
            # Konversi ke YUV
            yuv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2YUV)
            
            # Equalkan channel Y (luminance)
            yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
            
            # Konversi kembali ke BGR
            equalized = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
            
            self.processed_image = equalized
            self.display_image(self.processed_image, self.processed_panel)
            
            self.update_status("Histogram equalization selesai")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan histogram equalization: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()