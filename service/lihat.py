from tkinter import *
from tkinter import ttk, messagebox
from pathlib import Path
from database import DatabaseManager

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / Path(r"assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class PageLihatTransaksi:
    def __init__(self, window):
        self.window = window
        self.window.title("Lihat Transaksi")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.db = DatabaseManager()

        # Canvas
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=765,
            width=412,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background
        self.bg_image = PhotoImage(file=relative_to_assets("Lihat2.png"))
        self.canvas.create_image(206.0, 400.0, image=self.bg_image)

        # Tombol kembali
        self.btn_kembali_img = PhotoImage(file=relative_to_assets("btnKembali.png"))
        Button(
            self.window,
            image=self.btn_kembali_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.window.destroy,
            relief="flat"
        ).place(x=13.0, y=35.0, width=100.0, height=22.188)

        # Frame scrollable
        self.scroll_canvas = Canvas(self.window, bg="#F1F1F1", bd=0, highlightthickness=0)
        self.scroll_frame = Frame(self.scroll_canvas, bg="#F1F1F1")
        self.scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.scroll_canvas.yview)

        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        self.scroll_canvas.place(x=10, y=155, width=412, height=570)
        self.scrollbar.place(x=390, y=155, height=570)

        # Load transaksi
        self.load_data()

    def load_data(self):
        try:
            for widget in self.scroll_frame.winfo_children():
                    widget.destroy()

            transaksi_list = self.db.get_all_transaksi()

            if not transaksi_list:
                self.info_label.config(text="Tidak ada transaksi yang ditemukan", fg="red")
                return

            panel_img = PhotoImage(file=relative_to_assets("Panel.png"))
            # index_img = PhotoImage(file=relative_to_assets("Circle.png"))
            self.panel_img = []
            # self.index_img = []
            i = 0
            for transaksi in transaksi_list:
                panel_frame = Frame(self.scroll_frame, width=panel_img.width(), height=panel_img.height(), bg="#FFFFFF")
                panel_frame.pack(pady=5)
                panel_frame.pack_propagate(False)

                # Tambah canvas di atas panel_frame untuk garis
                canvas = Canvas(panel_frame, width=panel_img.width(), height=panel_img.height(), bg="#FFFFFF", highlightthickness=0)
                canvas.place(x=0, y=0)

                # Background label
                bg_label = Label(panel_frame, image=panel_img)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                # Tampilkan transaksi[0] di atas circle
                circle_text = Label(panel_frame, text=str(transaksi[0]), font=("Arial", 10, "bold"), bg="#FFFFFF", fg="#000")
                circle_text.place(x=35, y=30)  # Sesuaikan posisi agar teks ada di tengah gambar bulat

                # Warna teks jumlah tergantung jenis
                warna_teks = "#138A36" if transaksi[1] == "Pemasukan" else "#B22222"

                # Frame isi konten di samping kanan circle
                isi_frame = Frame(panel_frame, bg="#FFFFFF")
                isi_frame.place(x=70, y=26)

                self.panel_img.append(panel_img)

                Label(isi_frame, text=f"Jenis: {transaksi[1]}", font=("Arial", 10), bg="#FFFFFF", fg=warna_teks).grid(row=0, column=0, sticky="w", padx=10)
                Label(isi_frame, text=f"Kategori: {transaksi[2]}", font=("Arial", 10), bg="#FFFFFF").grid(row=1, column=0, sticky="w", padx=10)
                Label(isi_frame, text=f"Jumlah: Rp {transaksi[3]:,.0f}", font=("Arial", 10), bg="#FFFFFF").grid(row=2, column=0, sticky="w", padx=10)
                Label(isi_frame, text=f"Tanggal: {transaksi[4]}", font=("Arial", 10), bg="#FFFFFF").grid(row=3, column=0, sticky="w", padx=10)
                Label(isi_frame, text=f"Deskripsi: {transaksi[5] if transaksi[5] else 'Tidak ada'}", font=("Arial", 10), bg="#FFFFFF", wraplength=300, justify="left").grid(row=4, column=0, sticky="w", padx=10)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")