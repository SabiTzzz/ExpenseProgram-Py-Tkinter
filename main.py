from tkinter import Tk, Canvas, Button, PhotoImage, Toplevel
from pathlib import Path
from service.tambah import PageTambahTransaksi
from service.edit import PageEditTransaksi
from service.hapus import PageHapusTransaksi
from service.lihat import PageLihatTransaksi
from service.laporan import PageLaporan
from database import DatabaseManager

OUTPUT_PATH = Path(__file__).parent 
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("412x752")
        self.root.configure(bg="#F1F1F1")
        self.root.resizable(False, False)
        
        # Initialize database
        self.db = DatabaseManager()
        
        self.canvas = Canvas(   
            root,
            bg="#F1F1F1",
            height=752,
            width=412,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.setup_ui()
    
    def setup_ui(self):
        # Load Gambar
        self.image = PhotoImage(file=relative_to_assets("Home.png"))
        self.canvas.create_image(206.0, 376.0, image=self.image)

        # Button Keluar
        self.button_keluar = PhotoImage(file=relative_to_assets("btnKeluar.png"))
        Button(image=self.button_keluar, borderwidth=0, command=self.keluar).place(x=225.0, y=591.0, width=150.0, height=120.0)

        # Button Tambah Transaksi
        self.btn_tambah = PhotoImage(file=relative_to_assets("btnTambah.png"))
        Button(image=self.btn_tambah, borderwidth=0, command=self.tambah_transaksi).place(x=37.0, y=286.0, width=150.0, height=120.0)

        # Button Lihat Transaksi
        self.button_lihat = PhotoImage(file=relative_to_assets("btnLihat.png"))
        Button(image=self.button_lihat, borderwidth=0, command=self.lihat_transaksi).place(x=225.0, y=286.0, width=150.0, height=120.0)

        # Button Edit Transaksi
        self.button_edit = PhotoImage(file=relative_to_assets("btnEdit.png"))
        Button(image=self.button_edit, borderwidth=0, command=self.edit_transaksi).place(x=37.0, y=438.0, width=150.0, height=120.0)

        # Button Hapus Transaksi
        self.button_hapus = PhotoImage(file=relative_to_assets("btnHapus.png"))
        Button(image=self.button_hapus, borderwidth=0, command=self.hapus_transaksi).place(x=225.0, y=438.0, width=150.0, height=120.0)

        # Button Laporan
        self.button_laporan = PhotoImage(file=relative_to_assets("btnLaporan.png"))
        Button(image=self.button_laporan, borderwidth=0, command=self.laporan).place(x=37.0, y=591, width=150.0, height=120.0)
    
    @staticmethod
    def center_window(window, width=412, height=752):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def keluar(self):
        self.root.destroy()
    
    def tambah_transaksi(self):
        tambah_window = Toplevel(self.root)
        PageTambahTransaksi(tambah_window)
        self.center_window(tambah_window, 412, 752)

    def edit_transaksi(self):
        edit_window = Toplevel(self.root)
        PageEditTransaksi(edit_window)
        self.center_window(edit_window, 412, 752)
    
    def lihat_transaksi(self):
        lihat_window = Toplevel(self.root)
        PageLihatTransaksi(lihat_window)
        self.center_window(lihat_window, 412, 752)
    
    def hapus_transaksi(self):
        hapus_window = Toplevel(self.root)
        PageHapusTransaksi(hapus_window)
        self.center_window(hapus_window, 412, 752)
    
    def laporan(self):
        laporan_window = Toplevel(self.root)
        PageLaporan(laporan_window)
        self.center_window(laporan_window, 412, 752)

if __name__ == "__main__":
    root = Tk()
    app = MainApp(root)
    MainApp.center_window(root)
    root.mainloop()