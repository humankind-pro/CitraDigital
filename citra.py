import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as style

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra Digital - F.A.I.T Vision")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1e1e2e')
        self.root.state('zoomed')  # Maximized window
        self.zoom_level = 1.0
        self.bind_zoom_events()
        
        # Style configuration
        self.setup_styles()
        
        # Image variables
        self.original_image = None
        self.processed_image = None
        self.current_image_path = None
        self.second_image = None
        self.second_image_path = None
        
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def bind_zoom_events(self):
        """Bind mouse wheel events for zooming"""
        if hasattr(self, 'processed_panel'):
            self.processed_panel.bind("<MouseWheel>", self.zoom_image)
            self.processed_panel.bind("<Button-4>", self.zoom_image)  # Linux zoom in
            self.processed_panel.bind("<Button-5>", self.zoom_image)  # Linux zoom out

    def setup_styles(self):
        """Setup modern styling"""
        style.use('dark_background')
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define color palette
        self.colors = {
            'bg_primary': '#1e1e2e',
            'bg_secondary': '#313244',
            'bg_tertiary': '#45475a',
            'accent': '#89b4fa',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'error': '#f38ba8',
            'text_primary': '#cdd6f4',
            'text_secondary': '#bac2de'
        }
    
    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_container)
        
        # Control panel
        self.create_control_panel(main_container)
        
        # Image display area
        self.create_image_display_area(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
        # Bind resize event
        self.root.bind("<Configure>", self.on_window_resize)
    
    def create_header(self, parent):
        """Create professional header"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🖼 APLIKASI PENGOLAHAN CITRA DIGITAL",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Sistem Pembelajaran Mata Kuliah Pencitraan Digital",
            font=('Segoe UI', 12),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack()
    
    def create_control_panel(self, parent):
        """Create modern control panel"""
        control_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        control_frame.pack(fill="x", pady=(0, 20))
        
        # File Operations
        self.create_file_operations_panel(control_frame)
        
        # Basic Processing
        self.create_basic_processing_panel(control_frame)
        
        # Advanced Filters
        self.create_advanced_filters_panel(control_frame)
    
    def create_file_operations_panel(self, parent):
        """File operations panel"""
        frame = tk.LabelFrame(
            parent,
            text="📁 Operasi File",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            bd=2
        )
        frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        
        buttons = [
            ("📂 Buka Gambar Utama", self.load_image, '#6B728E'),
            ("📂 Buka Gambar Kedua", self.load_second_image, '#6B728E'),
            ("💾 Simpan Hasil", self.save_processed_image, '#6B728E'),
            ("🔄 Reset Gambar", self.reset_image, '#6B728E')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                frame,
                text=text,
                command=command,
                font=('Segoe UI', 10),
                bg=color,
                fg='white',
                width=20,
                height=2,
                relief='flat',
                cursor='hand2'
            )
            btn.pack(pady=8, padx=10, fill="x")
            self.add_button_hover_effect(btn, color)
    
    def reset_zoom(self):
        """Reset zoom level to 1.0"""
        self.zoom_level = 1.0
        if self.processed_image is not None:
            self.display_image(self.processed_image, self.processed_panel)
        self.update_status("🔍 Zoom direset ke level normal")
    
    def create_basic_processing_panel(self, parent):
        """Basic processing panel"""
        frame = tk.LabelFrame(
            parent,
            text="🔧 Pemrosesan Dasar",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            bd=2
        )
        frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        
        buttons = [
            ("⚫ Grayscale", self.convert_to_grayscale, '#6c7086'),
            ("⚫ Citra Biner", self.convert_to_binary, '#6c7086'),
            ("⚫ Operasi Aritmatika (Tambah Kecerahan)", self.arithmetic_addition, '#6c7086'),
            ("⚫ Operasi Logika (AND)", self.logic_and_operation, "#6c7086"),
            ("⚫ Histogram (Gambar Input)", self.show_histogram, '#6c7086')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                frame,
                text=text,
                command=command,
                font=('Segoe UI', 10),
                bg=color,
                fg='white',
                width=20,
                height=2,
                relief='flat',
                cursor='hand2'
            )
            btn.pack(pady=5, padx=10, fill="x")
            self.add_button_hover_effect(btn, color)
    
    def create_advanced_filters_panel(self, parent):
        """Advanced filters panel"""
        frame = tk.LabelFrame(
            parent,
            text="✨ Filter & Efek Lanjutan",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            bd=2
        )
        frame.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
        
        buttons = [
            ("📐 Edge Detection", self.edge_detection, '#6B728E'),
            ("⚫ Dilasi Diagonal", self.dilation_diagonal, '#6B728E'),
            ("⚫ Dilasi Persegi", self.dilation_horizontal, '#6B728E')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                frame,
                text=text,
                command=command,
                font=('Segoe UI', 10),
                bg=color,
                fg='white',
                width=20,
                height=2,
                relief='flat',
                cursor='hand2'
            )
            btn.pack(pady=8, padx=10, fill="x")
            self.add_button_hover_effect(btn, color)
        
        # Configure grid weights
        for i in range(3):
            parent.columnconfigure(i, weight=1)
    
    def create_image_display_area(self, parent):
        """Create three-panel image display area"""
        display_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        display_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Original image panel
        original_frame = tk.LabelFrame(
            display_frame,
            text="🖼 Gambar Asli",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            bd=2
        )
        original_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.original_panel = tk.Label(
            original_frame,
            text="Klik 'Buka Gambar Utama' untuk memulai",
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 11),
            width=30,
            height=15
        )
        self.original_panel.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Second image panel
        second_frame = tk.LabelFrame(
            display_frame,
            text="🖼 Gambar Kedua",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            bd=2
        )
        second_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.second_panel = tk.Label(
            second_frame,
            text="Klik 'Buka Gambar Kedua' untuk operasi logika",
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 11),
            width=30,
            height=15
        )
        self.second_panel.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Processed image panel
        processed_frame = tk.LabelFrame(
            display_frame,
            text="✨ Hasil Pemrosesan",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            bd=2
        )
        processed_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.processed_panel = tk.Label(
            processed_frame,
            text="Hasil pemrosesan akan muncul di sini",
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            font=('Segoe UI', 11),
            width=30,
            height=15
        )
        self.processed_panel.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Configure grid weights
        for i in range(3):
            display_frame.columnconfigure(i, weight=1)
        display_frame.rowconfigure(0, weight=1)
    
    def create_status_bar(self, parent):
        """Create modern status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=40)
        status_frame.pack(fill="x")
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 IK23-C - F.A.I.T Vision")
        
        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 10),
            anchor="w"
        )
        status_label.pack(fill="x", padx=15, pady=10)
    
    def add_button_hover_effect(self, button, original_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=self.lighten_color(original_color))
        
        def on_leave(e):
            button.config(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def lighten_color(self, color):
        """Lighten a color for hover effect"""
        if not color.startswith('#'):
            return color
        # Convert hex to RGB
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # Lighten by increasing each component
        r = min(255, int(r * 1.2))
        g = min(255, int(g * 1.2))
        b = min(255, int(b * 1.2))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def update_status(self, message):
        """Update status bar with message"""
        self.status_var.set(f"🔄 {message}")
        self.root.update_idletasks()
    
    def on_window_resize(self, event):
        """Handle window resize"""
        if event.widget == self.root:
            self.root.after(100, self._update_displayed_images)
    
    def _check_image_loaded(self):
        """Check if main image is loaded"""
        if self.original_image is None:
            messagebox.showerror(
                "❌ Error", 
                "Tidak ada gambar yang dimuat.\nSilakan buka gambar utama terlebih dahulu.",
                parent=self.root
            )
            return False
        return True
    
    def dilation_diagonal(self):
        """Dilasi dengan Structuring Element berbentuk diagonal"""
        if not self._check_image_loaded():
            return
        try:
            # Convert to grayscale and threshold if needed
            if len(self.original_image.shape) == 3:
                gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            else:
                _, binary = cv2.threshold(self.original_image, 127, 255, cv2.THRESH_BINARY)
            
            # Define diagonal kernel
            kernel_diag = np.array([[1, 0, 1], 
                                [0, 1, 0], 
                                [1, 0, 1]], dtype=np.uint8)
            
            # Apply dilation
            dilated = cv2.dilate(binary, kernel_diag, iterations=1)
            
            self.processed_image = dilated
            self.display_image(dilated, self.processed_panel)
            self.update_status("✅ Dilasi dengan kernel diagonal selesai")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan dilasi diagonal:\n{str(e)}")

    def dilation_horizontal(self):
        """Dilasi dengan Structuring Element berbentuk horizontal"""
        if not self._check_image_loaded():
            return
        try:
            # Convert to grayscale and threshold if needed
            if len(self.original_image.shape) == 3:
                gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            else:
                _, binary = cv2.threshold(self.original_image, 127, 255, cv2.THRESH_BINARY)
            
            # Define horizontal kernel
            kernel_horizontal = np.array([[0, 0, 0], 
                                        [1, 1, 1], 
                                        [0, 0, 0]], dtype=np.uint8)
            
            # Apply dilation
            dilated = cv2.dilate(binary, kernel_horizontal, iterations=1)
            
            self.processed_image = dilated
            self.display_image(dilated, self.processed_panel)
            self.update_status("✅ Dilasi dengan kernel horizontal selesai")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal melakukan dilasi horizontal:\n{str(e)}")

    def _check_two_images_loaded(self):
        """Check if both images are loaded"""
        if self.original_image is None or self.second_image is None:
            messagebox.showerror(
                "❌ Error", 
                "Diperlukan dua gambar untuk operasi ini.\nPastikan gambar utama dan gambar kedua sudah dimuat.",
                parent=self.root
            )
            return False
        if self.original_image.shape != self.second_image.shape:
            messagebox.showerror(
                "❌ Error", 
                "Ukuran atau jumlah channel kedua gambar harus sama.",
                parent=self.root
            )
            return False
        return True
    
    def _load_image_with_pil_fallback(self, path):
        """Load image with PIL fallback"""
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
            raise ValueError(f"Tidak dapat memuat gambar dari: {os.path.basename(path)}.\nError: {str(e)}")
    
    def load_image(self):
        """Load main image"""
        file_types = [
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.heic"),
            ("All files", ".")
        ]
        path = filedialog.askopenfilename(
            title="Pilih Gambar Utama",
            filetypes=file_types,
            parent=self.root
        )
        if not path:
            return
        
        try:
            self.current_image_path = path
            self.original_image = self._load_image_with_pil_fallback(path)
            self.display_image(self.original_image, self.original_panel)
            
            # Reset processed image
            self.processed_image = None
            self.processed_panel.config(
                image='',
                text="Hasil pemrosesan akan muncul di sini"
            )
            self.processed_panel.image = None
            
            self.update_status(f"✅ Gambar utama dimuat: {os.path.basename(path)}")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Terjadi kesalahan saat memuat gambar:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal memuat gambar utama")
    
    def load_second_image(self):
        """Load second image for logic operations"""
        if not self._check_image_loaded():
            return
        
        file_types = [
            ("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp *.heic"),
            ("All files", ".")
        ]
        path = filedialog.askopenfilename(
            title="Pilih Gambar Kedua",
            filetypes=file_types,
            parent=self.root
        )
        if not path:
            return
        
        try:
            second_img = self._load_image_with_pil_fallback(path)
            
            # Resize to match original image
            h, w = self.original_image.shape[:2]
            second_img = cv2.resize(second_img, (w, h), interpolation=cv2.INTER_AREA)
            
            # Match color channels
            if len(self.original_image.shape) == 3 and len(second_img.shape) == 2:
                second_img = cv2.cvtColor(second_img, cv2.COLOR_GRAY2BGR)
            elif len(self.original_image.shape) == 2 and len(second_img.shape) == 3:
                second_img = cv2.cvtColor(second_img, cv2.COLOR_BGR2GRAY)
            
            self.second_image = second_img
            self.second_image_path = path
            self.display_image(second_img, self.second_panel)
            
            self.update_status(f"✅ Gambar kedua dimuat: {os.path.basename(path)}")
            messagebox.showinfo(
                "✅ Sukses", 
                "Gambar kedua berhasil dimuat!\nSekarang Anda dapat melakukan operasi logika.",
                parent=self.root
            )
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Terjadi kesalahan saat memuat gambar kedua:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal memuat gambar kedua")
    
    def display_image(self, image_cv, panel, zoom=None):
        """Display image in panel while maintaining aspect ratio"""
        if image_cv is None:
            panel.config(image='', text="Tidak ada gambar")
            panel.image = None
            return
        
        try:
            # Dapatkan ukuran asli gambar
            original_height, original_width = image_cv.shape[:2]
            aspect_ratio = original_width / original_height
            
            # Dapatkan ukuran panel yang tersedia
            panel_width = panel.winfo_width()
            panel_height = panel.winfo_height()
            
            # Hitung ukuran baru yang mempertahankan aspect ratio
            if panel_width / aspect_ratio < panel_height:
                new_width = panel_width
                new_height = int(panel_width / aspect_ratio)
            else:
                new_height = panel_height
                new_width = int(panel_height * aspect_ratio)
            
            # Pastikan ukuran minimal 1 pixel
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
            # Resize gambar dengan interpolasi yang baik
            resized_image = cv2.resize(image_cv, (new_width, new_height), 
                                    interpolation=cv2.INTER_AREA)
            
            # Konversi ke format yang bisa ditampilkan di Tkinter
            if len(resized_image.shape) == 2:  # Grayscale
                image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
            else:  # Color (BGR)
                image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
            
            # Konversi ke PhotoImage
            image_pil = Image.fromarray(image_rgb)
            photo = ImageTk.PhotoImage(image_pil)
            
            # Update panel
            panel.image = photo
            panel.config(image=photo, text="")
            
        except Exception as e:
            panel.config(image='', text=f"Error menampilkan gambar:\n{str(e)}")
            panel.image = None
            self.update_status(f"❌ Gagal menampilkan gambar: {str(e)}")

    def zoom_image(self, event):
        """Handle zoom in/out for processed image"""
        if self.processed_image is None:
            return
        
        # Determine zoom direction
        if event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):  # Zoom out
            self.zoom_level = max(0.1, self.zoom_level * 0.9)
        else:  # Zoom in
            self.zoom_level = min(3.0, self.zoom_level * 1.1)
        
        # Apply zoom
        self.display_image(self.processed_image, self.processed_panel, zoom=self.zoom_level)
        self.update_status(f"🔍 Zoom level: {self.zoom_level:.1f}x")
    
    def _update_displayed_images(self):
        """Update all displayed images"""
        if self.original_image is not None:
            self.display_image(self.original_image, self.original_panel)
        if self.second_image is not None:
            self.display_image(self.second_image, self.second_panel)
        if self.processed_image is not None:
            self.display_image(self.processed_image, self.processed_panel)
    
    def reset_image(self):
        """Reset all images to original state"""
        if not self.current_image_path:
            messagebox.showwarning(
                "⚠ Peringatan", 
                "Tidak ada gambar asli untuk di-reset.",
                parent=self.root
            )
            return
        
        try:
            # Clear all images
            self.original_image = None
            self.processed_image = None
            self.second_image = None
            self.second_image_path = None
            
            # Reset current image path
            self.current_image_path = None
            
            # Clear all panels
            self.original_panel.config(image='', text="Klik 'Buka Gambar Utama' untuk memulai")
            self.original_panel.image = None
            
            self.processed_panel.config(image='', text="Hasil pemrosesan akan muncul di sini")
            self.processed_panel.image = None
            
            self.second_panel.config(image='', text="Klik 'Buka Gambar Kedua' untuk operasi logika")
            self.second_panel.image = None
            
            self.update_status("🔄 Semua gambar telah direset")
            messagebox.showinfo(
                "✅ Reset Berhasil", 
                "Semua gambar telah dihapus. Silakan buka gambar baru.",
                parent=self.root
            )
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal me-reset gambar:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal me-reset gambar")
        
    def save_processed_image(self):
        """Save processed image"""
        if self.processed_image is None:
            messagebox.showerror(
                "❌ Error", 
                "Tidak ada gambar hasil proses untuk disimpan.",
                parent=self.root
            )
            return
        
        file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff"),
            ("All files", ".")
        ]
        path = filedialog.asksaveasfilename(
            title="Simpan Gambar Hasil",
            defaultextension=".png",
            filetypes=file_types,
            parent=self.root
        )
        if not path:
            return
        
        try:
            save_img = self.processed_image.copy()
            
            # Convert grayscale to BGR for certain formats
            if len(save_img.shape) == 2 and path.lower().endswith(('.jpg', '.jpeg', '.webp')):
                save_img = cv2.cvtColor(save_img, cv2.COLOR_GRAY2BGR)
            
            cv2.imwrite(path, save_img)
            self.update_status(f"💾 Gambar disimpan: {os.path.basename(path)}")
            messagebox.showinfo(
                "✅ Sukses", 
                f"Gambar berhasil disimpan di:\n{path}",
                parent=self.root
            )
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Terjadi kesalahan saat menyimpan:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal menyimpan gambar")
    
    # === IMAGE PROCESSING METHODS ===
    
    def convert_to_grayscale(self):
        """Convert image to grayscale"""
        if not self._check_image_loaded():
            return
        
        try:
            if len(self.original_image.shape) == 3:
                gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = self.original_image.copy()
            
            self.processed_image = gray_image
            self.display_image(gray_image, self.processed_panel)
            self.update_status("✅ Konversi ke grayscale selesai")
            self.zoom_level = 1.0  # Reset zoom
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal mengkonversi ke grayscale:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal mengkonversi ke grayscale")
    
    def convert_to_binary(self):
        """Convert image to binary"""
        if not self._check_image_loaded():
            return
        
        try:
            threshold_str = simpledialog.askstring(
                "Input Threshold", 
                "Masukkan nilai threshold (0-255):",
                initialvalue="127",
                parent=self.root
            )
            
            if threshold_str is None:
                return
            
            try:
                threshold = int(threshold_str)
                threshold = max(0, min(255, threshold))
            except ValueError:
                threshold = 127
                messagebox.showwarning(
                    "⚠ Input", 
                    "Nilai tidak valid, menggunakan threshold default (127)",
                    parent=self.root
                )
            
            # Convert to grayscale first if needed
            if len(self.original_image.shape) == 3:
                gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = self.original_image.copy()
            
            # Apply threshold
            _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
            
            self.processed_image = binary_image
            self.display_image(binary_image, self.processed_panel)
            self.update_status(f"✅ Konversi ke biner selesai (threshold: {threshold})")
            self.zoom_level = 1.0  # Reset zoom
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal mengkonversi ke biner:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal mengkonversi ke biner")
    
    def arithmetic_addition(self):
        """Add brightness to image"""
        if not self._check_image_loaded():
            return
        
        try:
            value_str = simpledialog.askstring(
                "Input Kecerahan", 
                "Masukkan nilai penambah kecerahan (0-255):",
                initialvalue="50",
                parent=self.root
            )
            
            if value_str is None:
                return
            
            try:
                value = int(value_str)
                value = max(0, min(255, value))
            except ValueError:
                value = 50
                messagebox.showwarning(
                    "⚠ Input", 
                    "Nilai tidak valid, menggunakan nilai default (50)",
                    parent=self.root
                )
            
            # Create matrix with brightness value
            M = np.ones(self.original_image.shape, dtype="uint8") * value
            added_image = cv2.add(self.original_image, M)
            
            self.processed_image = added_image
            self.display_image(added_image, self.processed_panel)
            self.update_status(f"✅ Kecerahan ditambah: +{value}")
            self.zoom_level = 1.0  # Reset zoom
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menambah kecerahan:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal menambah kecerahan")
    
    def morphological_erosion(self):
        """Apply morphological erosion"""
        if not self._check_image_loaded():
            return
        
        try:
            # Convert to grayscale if needed
            if len(self.original_image.shape) == 3:
                img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            else:
                img = self.original_image.copy()
            
            # Define structuring elements
            se1 = np.array([[1, 1, 1],
                           [1, 1, 1],
                           [1, 1, 1]], dtype=np.uint8)  # Square 3x3
            se2 = np.array([[0, 1, 0],
                           [1, 1, 1],
                           [0, 1, 0]], dtype=np.uint8)  # Cross 3x3
            
            # Apply erosion
            eroded_image1 = cv2.erode(img, se1)
            eroded_image2 = cv2.erode(img, se2)
            eroded_image = cv2.bitwise_or(eroded_image1, eroded_image2)
            
            # Convert back to BGR if original was color
            if len(self.original_image.shape) == 3:
                eroded_image = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2BGR)
            
            self.processed_image = eroded_image
            self.display_image(self.processed_image, self.processed_panel)
            self.update_status("✅ Operasi erosi selesai")
            self.zoom_level = 1.0  # Reset zoom
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal melakukan operasi erosi:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal melakukan operasi erosi")
    
    def show_histogram(self):
        """Show histogram of the original image"""
        if not self._check_image_loaded():
            return
        
        try:
            plt.figure(figsize=(8, 4))
            colors = ('b', 'g', 'r')
            
            # Handle grayscale or color images
            if len(self.original_image.shape) == 2:
                hist = cv2.calcHist([self.original_image], [0], None, [256], [0, 256])
                plt.plot(hist, color='gray')
            else:
                for i, color in enumerate(colors):
                    hist = cv2.calcHist([self.original_image], [i], None, [256], [0, 256])
                    plt.plot(hist, color=color)
            
            plt.title('Histogram Gambar', fontsize=12)
            plt.xlabel('Intensitas Pixel', fontsize=10)
            plt.ylabel('Jumlah Pixel', fontsize=10)
            plt.xlim([0, 256])
            
            if len(self.original_image.shape) == 3:
                plt.legend(['B', 'G', 'R'])
            
            plt.grid(True, alpha=0.3)
            plt.show()
            self.update_status("📊 Histogram ditampilkan")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal menampilkan histogram:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal menampilkan histogram")
    
    def edge_detection(self):
        """Apply Canny edge detection"""
        if not self._check_image_loaded():
            return
        
        try:
            # Convert to grayscale
            if len(self.original_image.shape) == 3:
                gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            else:
                gray = self.original_image.copy()
            
            # Apply Canny
            edges = cv2.Canny(gray, 100, 200)
            
            # Convert back to BGR for display consistency
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            self.processed_image = edges_bgr
            self.display_image(edges_bgr, self.processed_panel)
            self.update_status("✅ Deteksi tepi (Canny) selesai")
            self.zoom_level = 1.0  # Reset zoom
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal melakukan deteksi tepi:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal melakukan deteksi tepi")
    
    def logic_and_operation(self):
        """Apply AND operation on two images"""
        if not self._check_two_images_loaded():
            return
        
        try:
            and_result = cv2.bitwise_and(self.original_image, self.second_image)
            self.processed_image = and_result
            self.display_image(and_result, self.processed_panel)
            self.update_status("✅ Operasi AND selesai")
            self.zoom_level = 1.0  # Reset zoom
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal melakukan operasi AND:\n{str(e)}", parent=self.root)
            self.update_status("❌ Gagal melakukan operasi AND")
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?", parent=self.root):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()