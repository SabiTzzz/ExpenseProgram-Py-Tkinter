from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from pathlib import Path
from abc import ABC, abstractmethod

class BasePage(ABC):
    """Base class untuk semua page dalam aplikasi"""
    
    def __init__(self, root, title="Page", width=412, height=752):
        self.root = root
        self.width = width
        self.height = height
        self.title = title
        
        # Setup window
        self.setup_window()
        
        # Canvas utama
        self.canvas = Canvas(
            root,
            bg="#F1F1F1",
            height=height,
            width=width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
        # Dictionary untuk menyimpan image references
        self.images = {}
        
        # Setup UI
        self.setup_ui()
    
    def setup_window(self):
        """Setup basic window properties"""
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="#F1F1F1")
        self.root.resizable(False, False)
        self.center_window()
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
    
    @abstractmethod
    def setup_ui(self):
        """Abstract method untuk setup UI - harus diimplementasi di child class"""
        pass
    
    def load_image(self, image_name, image_path):
        """Load dan simpan image untuk mencegah garbage collection"""
        try:
            self.images[image_name] = PhotoImage(file=image_path)
            return self.images[image_name]
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return None
    
    def create_header(self, title_text, show_back_button=True):
        """Create standard header dengan title dan back button"""
        # Background header
        self.canvas.create_rectangle(0, 0, self.width, 80, fill="#2E7D32", outline="")
        
        # Title
        self.canvas.create_text(
            self.width // 2, 40,
            text=title_text,
            fill="white",
            font=("Arial", 16, "bold")
        )
        
        # Back button
        if show_back_button:
            self.create_back_button()
    
    def create_back_button(self):
        """Create back button"""
        back_button = Button(
            self.root,
            text="← Kembali",
            bg="#1B5E20",
            fg="white",
            font=("Arial", 10),
            borderwidth=0,
            command=self.back_action,
            cursor="hand2"
        )
        back_button.place(x=10, y=25, width=80, height=30)
    
    def back_action(self):
        """Default back action - close window"""
        self.root.destroy()
    
    def show_success_message(self, message):
        """Show success message"""
        messagebox.showinfo("Berhasil", message)
    
    def show_error_message(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
    
    def show_warning_message(self, message):
        """Show warning message"""
        messagebox.showwarning("Peringatan", message)
    
    def ask_confirmation(self, message):
        """Ask for confirmation"""
        return messagebox.askyesno("Konfirmasi", message)
    
    def validate_required_fields(self, fields_dict):
        """Validate required fields"""
        for field_name, field_value in fields_dict.items():
            if not field_value or str(field_value).strip() == "":
                self.show_error_message(f"Field {field_name} harus diisi!")
                return False
        return True
    
    def format_currency(self, amount):
        """Format number as currency"""
        return f"Rp {amount:,.0f}".replace(",", ".")
    
    def clear_canvas_area(self, x1, y1, x2, y2):
        """Clear specific area in canvas"""
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F1F1F1", outline="#F1F1F1")