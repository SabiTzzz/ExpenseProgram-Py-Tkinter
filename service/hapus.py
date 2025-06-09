from tkinter import *
from tkinter import messagebox, ttk
from database import DatabaseManager
from pathlib import Path

# Path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / Path(r"assets/frame0")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class PageHapusTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Hapus Transaksi")
        self.root.configure(bg="#F1F1F1")
        
        self.db = DatabaseManager()
        
        # Canvas
        self.canvas = Canvas(
            self.root,
            bg="#F1F1F1",
            height=752,
            width=412,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        self.bg_image = PhotoImage(file=relative_to_assets("Hapus.png"))
        self.canvas.create_image(206.0, 376.0, image=self.bg_image)

        # Tombol kembali
        self.btn_kembali_img = PhotoImage(file=relative_to_assets("btnKembali.png"))
        Button(
            self.root,
            image=self.btn_kembali_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.root.destroy,
            relief="flat"
        ).place(x=13.0, y=35.0, width=100.0, height=22.188)

        # Textbox
        self.bgtxt_id = PhotoImage(file=relative_to_assets("txtbox.png"))
        self.txt_id_frame = self.canvas.create_image(132, 713.5, image=self.bgtxt_id)
        self.txtid = Entry(self.canvas, font=("Arial", 12), relief="flat")
        self.txtid.place(x=58, y=695.0, width=147, height=35)

        # Button hapus
        self.btn_hapus_img = PhotoImage(file=relative_to_assets("btnHps.png"))
        Button(self.root, image=self.btn_hapus_img, borderwidth=0, bg="#369394", command=self.hapus_transaksi, relief="flat").place(x=262, y=695, width=95, height=37)

        self.scroll_canvas = Canvas(self.root, bg="#F1F1F1", bd=0, highlightthickness=0)
        self.scroll_frame = Frame(self.scroll_canvas, bg="#F1F1F1")
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.scroll_canvas.yview)

        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        self.scroll_canvas.place(x=10, y=155, width=412, height=480)
        self.scrollbar.place(x=390, y=155, height=480)
        
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
    
    def show_konfirmasi_hapus(self, id_int):
        popup = Toplevel(self.root)
        popup.title("Konfirmasi Hapus")
        popup.geometry("412x752")
        popup.configure(bg="#F1F1F1")
        popup.resizable(False, False)

        # Image background
        image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        canvas_popup = Canvas(popup, bg="#F1F1F1", height=752, width=412, highlightthickness=0)
        canvas_popup.pack()
        canvas_popup.create_image(203.0, 419.0, image=image_image_2)
        popup.image_image_2 = image_image_2  # agar tidak garbage collected

        # Tombol YA
        button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        button_2 = Button(
            popup,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.confirm_hapus(popup, id_int)
        )
        button_2.place(x=78.0, y=411.0, width=140.07, height=53.19)
        popup.button_image_2 = button_image_2

        # Tombol TIDAK
        button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        button_3 = Button(
            popup,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=popup.destroy
        )
        button_3.place(x=230.48, y=412.66, width=97.52, height=53.19)
        popup.button_image_3 = button_image_3

    def confirm_hapus(self, popup, id_int):
        try:
            self.db.hapus_transaksi(id_int)
            messagebox.showinfo("Sukses", f"Transaksi dengan ID {id_int} berhasil dihapus!")
            self.load_data()
            popup.destroy()
            self.txtid.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus transaksi: {str(e)}")

    def hapus_transaksi(self):
        id_transaksi = self.txtid.get().strip()
        if not id_transaksi or self.txtid.delete(0, END):
            messagebox.showerror("Error", "ID Transaksi harus diisi!")
            return

        try:
            id_int = int(id_transaksi)
        except ValueError:
            messagebox.showerror("Error", "ID Transaksi harus berupa angka!")
            return

        # Cek apakah ID ada di database
        if not self.db.cek_id_transaksi(id_int):    
            messagebox.showerror("Error", f"Transaksi dengan ID {id_int} tidak ditemukan!")
            return

        # Konfirmasi hapus
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus transaksi dengan ID {id_int}?")
        if not confirm:
            return

        try:
            self.db.hapus_transaksi(id_int)
            messagebox.showinfo("Sukses", f"Transaksi dengan ID {id_int} berhasil dihapus!")
            self.load_data()
            self.txtid.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus transaksi: {str(e)}")
