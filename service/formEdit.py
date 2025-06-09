from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from database import DatabaseManager
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class PageFormEditTransaksi:
    def __init__(self, root, id_transaksi):
        self.root = root
        self.root.title("Form Edit Transaksi")
        self.root.geometry("412x752")
        self.root.configure(bg="#F1F1F1")
        self.root.resizable(False, False)
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
        
        self.db = DatabaseManager()
        self.selected_id = id_transaksi
        self.load_transaksi_detail(id_transaksi)

    def setup_ui(self):
        self.image_bg = PhotoImage(file=relative_to_assets("FormEdit.png"))
        self.canvas.create_image(206.0, 376.0, image=self.image_bg)

        # Tombol kembali
        self.btn_kembali_img = PhotoImage(file=relative_to_assets("btnKembali.png"))
        Button(
            self.canvas,
            image=self.btn_kembali_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.root.destroy,
            relief="flat"
        ).place(x=13.0, y=35.0, width=100.0, height=22.188)

        # Tombol simpan
        self.btn_simpan_img = PhotoImage(file=relative_to_assets("btnSimpan.png"))
        Button(
            self.canvas,
            image=self.btn_simpan_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.simpan_perubahan,
            relief="flat"
        ).place(x=289, y=672.0, width=108.0, height=30.0)

        # Deskripsi (Text)
        self.entry_image_1 = PhotoImage(file=relative_to_assets("textarea.png"))
        self.canvas.create_image(205.0, 581.0, image=self.entry_image_1)
        self.deskripsi_text = Text(
            self.canvas, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.deskripsi_text.place(x=55.0, y=530.0, width=300.0, height=100.0)

        # Jumlah
        self.jumlah_var = StringVar()
        self.entry_image_2 = PhotoImage(file=relative_to_assets("txtJumlah.png"))
        self.canvas.create_image(205.0, 388.0, image=self.entry_image_2)
        self.jumlah_entry = Entry(
            self.canvas, textvariable=self.jumlah_var, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.jumlah_entry.place(x=55.0, y=372.0, width=300.0, height=30.0)

        # Kategori
        self.entry_image_3 = PhotoImage(file=relative_to_assets("txtKategori.png"))
        self.canvas.create_image(205.0, 310.0, image=self.entry_image_3)
        self.kategori_var = StringVar()
        self.kategori_entry = Entry(
            self.canvas, textvariable=self.kategori_var, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.kategori_entry.place(x=55.0, y=294.0, width=300.0, height=30.0)

        # Tanggal
        self.entry_image_4 = PhotoImage(file=relative_to_assets("txtTanggal.png"))
        self.canvas.create_image(205.0, 469.0, image=self.entry_image_4)
        self.tanggal_var = StringVar()
        self.tanggal_entry = Entry(
            self.canvas, textvariable=self.tanggal_var, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0
        )
        self.tanggal_entry.place(x=55.0, y=453.0, width=300.0, height=30.0)
        self.tanggal_var.set(datetime.now().strftime("%d-%m-%Y"))

        # Jenis transaksi (Combobox)
        self.jenis_var = StringVar()
        self.jenis_combo = ttk.Combobox(
            self.canvas,
            textvariable=self.jenis_var,
            values=["Pemasukan", "Pengeluaran"],
            state="readonly"
        )
        self.jenis_combo.place(x=55.0, y=210.0, width=300.0, height=32.0)

    def load_transaksi_detail(self, transaksi_id):
        try:
            # Get detailed data from database
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transaksi WHERE id = ?', (transaksi_id,))
            transaksi = cursor.fetchone()
            conn.close()
            
            if transaksi:
                # self.selected_id = transaksi[0]
                
                # Fill form fields
                # self.id_var.set(str(transaksi[0]))
                self.jenis_var.set(transaksi[1])
                self.kategori_var.set(transaksi[2])
                self.jumlah_var.set(str(transaksi[3]))
                self.tanggal_var.set(transaksi[4])
                
                # Clear and set description
                self.deskripsi_text.delete(1.0, END)
                if transaksi[5]:
                    self.deskripsi_text.insert(1.0, transaksi[5])
                
                # self.status_label.config(text=f"Editing transaksi ID: {transaksi[0]}", fg="blue")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat detail: {str(e)}")
    
    def simpan_perubahan(self):
        # if not self.selected_id:
        #     messagebox.showwarning("Warning", "Pilih transaksi yang akan diedit!")
        #     return
        print("Simpan perubahan")
        try:
            # Validate input
            jenis = self.jenis_var.get()
            kategori = self.kategori_var.get().strip()
            jumlah = float(self.jumlah_var.get())
            tanggal = self.tanggal_var.get().strip()
            deskripsi = self.deskripsi_text.get(1.0, END).strip()
            
            if not kategori:
                messagebox.showerror("Error", "Kategori harus diisi!")
                return
            
            if not jenis:
                messagebox.showerror("Error", "Pilih jenis transaksi!")
                return
            
            # Confirm update
            if messagebox.askyesno("Konfirmasi", 
                                 f"Yakin ingin mengupdate transaksi ID {self.selected_id}?"):
                
                # Update database
                self.db.update_transaksi(self.selected_id, jenis, kategori, jumlah, tanggal, deskripsi)
                
                messagebox.showinfo("Sukses", "Transaksi berhasil diupdate!")
                
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {str(e)}")
