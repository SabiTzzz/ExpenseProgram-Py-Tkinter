from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from pathlib import Path
from database import DatabaseManager

class PageTambahTransaksi:
    def __init__(self, window):
        print("Memuat PageTambahTransaksi di window:", window)
        self.window = window
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.db = DatabaseManager()

        # Paths
        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH.parent / Path(r"assets/frame0")

        def relative_to_assets(path: str) -> Path:
            return self.ASSETS_PATH / Path(path)

        self.relative_to_assets = relative_to_assets

        # Canvas
        self.canvas_t = Canvas(
            self.window,
            bg="#FFFFFF",
            height=765,
            width=412,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas_t.place(x=0, y=0)

        # Background image
        self.image_bg = PhotoImage(file=self.relative_to_assets("Tambah.png"))
        self.canvas_t.create_image(206.0, 376.0, image=self.image_bg)

        # Tombol kembali
        self.btn_kembali_img = PhotoImage(file=self.relative_to_assets("btnKembali.png"))
        Button(
            self.window,
            image=self.btn_kembali_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.window.destroy,
            relief="flat"
        ).place(x=13.0, y=35.0, width=100.0, height=22.188)

        # Tombol simpan
        self.btn_simpan_img = PhotoImage(file=self.relative_to_assets("btnSimpan.png"))
        Button(
            self.window,
            image=self.btn_simpan_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.simpan_transaksi,
            relief="flat"
        ).place(x=86.0, y=692.0, width=108.0, height=30.0)

        # Tombol batal
        self.btn_batal_img = PhotoImage(file=self.relative_to_assets("btnBatal.png"))
        Button(
            self.window,
            image=self.btn_batal_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.window.destroy,
            relief="flat"
        ).place(x=224.0, y=692.0, width=108.0, height=30.0)

        # Deskripsi (Text)
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("textarea.png"))
        self.canvas_t.create_image(205.0, 581.0, image=self.entry_image_1)
        self.deskripsi_text = Text(
            self.window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.deskripsi_text.place(x=55.0, y=530.0, width=300.0, height=100.0)

        # Jumlah
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("txtJumlah.png"))
        self.canvas_t.create_image(205.0, 388.0, image=self.entry_image_2)
        self.jumlah_entry = Entry(
            self.window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.jumlah_entry.place(x=55.0, y=372.0, width=300.0, height=30.0)

        # Kategori
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("txtKategori.png"))
        self.canvas_t.create_image(205.0, 310.0, image=self.entry_image_3)
        self.kategori_entry = Entry(
            self.window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.kategori_entry.place(x=55.0, y=294.0, width=300.0, height=30.0)

        # Tanggal
        self.entry_image_4 = PhotoImage(file=self.relative_to_assets("txtTanggal.png"))
        self.canvas_t.create_image(205.0, 469.0, image=self.entry_image_4)
        self.tanggal_entry = Entry(
            self.window, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.tanggal_entry.place(x=55.0, y=453.0, width=300.0, height=30.0)
        self.tanggal_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))

        # Jenis transaksi (Combobox)
        self.jenis_var = StringVar(value="Pemasukan")
        self.jenis_combo = ttk.Combobox(
            self.window,
            textvariable=self.jenis_var,
            values=["Pemasukan", "Pengeluaran"],
            state="readonly"
        )
        self.jenis_combo.place(x=55.0, y=210.0, width=300.0, height=32.0)

    def simpan_transaksi(self):
        try:
            jenis = self.jenis_var.get()
            kategori = self.kategori_entry.get().strip()
            jumlah = float(self.jumlah_entry.get())
            tanggal = self.tanggal_entry.get().strip()
            deskripsi = self.deskripsi_text.get("1.0", END).strip()

            if not kategori:
                messagebox.showerror("Error", "Kategori harus diisi!")
                return

            self.db.tambah_transaksi(jenis, kategori, jumlah, tanggal, deskripsi)
            messagebox.showinfo("Sukses", "Transaksi berhasil ditambahkan!")
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")