from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from database import DatabaseManager
from service.formEdit import PageFormEditTransaksi
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH.parent / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class PageEditTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Transaksi")
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
        self.load_transaksi_list()

    def setup_ui(self):
        self.bgimage = PhotoImage(file=relative_to_assets("Edit.png"))
        self.canvas.create_image(206.0, 376.0, image=self.bgimage)

        Label(self.canvas, text="Masukkan ID Transaksi Yang Ingin Diubah", bg="#23A8AA", fg="#FFFFFF", font=("Arial", 10)).place(x=80, y=640.0)

        self.button_ubahId = PhotoImage(file=relative_to_assets("btnUbahId.png"))
        Button(self.root, image=self.button_ubahId, borderwidth=0, bg="#369394", command=lambda: self.form_edit_transaksi(self.txt_id.get()), relief="flat", highlightthickness=0).place(x=280.0, y=670.0, width=103.0, height=45.0)

        self.bgtxt_id = PhotoImage(file=relative_to_assets("Textbox.png"))
        self.txt_id_frame = self.canvas.create_image(120.0, 695.0, image=self.bgtxt_id)
        self.txt_id = Entry(self.canvas, font=("Arial", 12), width=20, relief="flat")
        self.txt_id.place(x=45, y=677.0, width=150, height=26)

        self.button_kembali = PhotoImage(file=relative_to_assets("btnKembali.png"))
        Button(
            self.root,
            image=self.button_kembali,
            borderwidth=0,
            highlightthickness=0,
            command=self.root.destroy,
            relief="flat"
        ).place(x=13.0, y=35.0, width=100.0, height=22.188)

        # Frame scrollable
        self.scroll_canvas = Canvas(self.root, bg="#F1F1F1", bd=0, highlightthickness=0)
        self.scroll_frame = Frame(self.scroll_canvas, bg="#F1F1F1")
        self.scrollbar = Scrollbar(self.root, orient=VERTICAL, command=self.scroll_canvas.yview)

        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )

        self.scroll_canvas.place(x=10, y=150, width=412, height=450)
        self.scrollbar.place(x=390, y=150, height=450)

    @staticmethod
    def center_window(window, width=412, height=752):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def form_edit_transaksi(self, id_transaksi):
        if not id_transaksi:
            messagebox.showwarning("Warning", "Masukkan ID transaksi yang valid!")
            return
        
        transaksi_list = self.db.get_all_transaksi()

        for transaksi in transaksi_list:
            if str(transaksi[0]) == id_transaksi:
                formEdit_window = Toplevel(self.root)
                PageFormEditTransaksi(formEdit_window, id_transaksi)
                self.center_window(formEdit_window)
                break
        else:
            messagebox.showwarning("Warning", "Transaksi tidak ditemukan!")

    def load_transaksi_list(self):
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

    def on_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            transaksi_id = item['values'][0]
            self.load_transaksi_detail(transaksi_id)
    
    def load_transaksi_detail(self, transaksi_id):
        try:
            # Get detailed data from database
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transaksi WHERE id = ?', (transaksi_id,))
            transaksi = cursor.fetchone()
            conn.close()
            
            if transaksi:
                jenis, kategori, jumlah, tanggal, deskripsi = transaksi
                
                # Fill form fields
                self.jenis_var.set(jenis)
                # Kategori
                self.kategori_entry.delete(0, 'end')
                self.kategori_entry.insert(0, kategori)
                # Jumlah
                self.jumlah_entry.delete(0, 'end')
                self.jumlah_entry.insert(0, str(jumlah))
                # Tanggal
                self.tanggal_entry.delete(0, 'end')
                self.tanggal_entry.insert(0, tanggal)
                # Deskripsi
                self.deskripsi_text.delete("1.0", "end")
                self.deskripsi_text.insert("1.0", deskripsi)
                # Set selected ID
                self.selected_id = transaksi_id
                
                self.status_label.config(text=f"Editing transaksi ID: {transaksi_id}", fg="blue")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat detail: {str(e)}")
    
    def simpan_perubahan(self):
        if not self.selected_id:
            messagebox.showwarning("Warning", "Pilih transaksi yang akan diedit!")
            return
        
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
                
                # Refresh list and reset form
                self.load_transaksi_list()
                self.reset_form()
                
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan: {str(e)}")
    
    def reset_form(self):
        self.selected_id = None
        self.id_var.set("")
        self.jenis_var.set("")
        self.kategori_var.set("")
        self.jumlah_var.set("")
        self.tanggal_var.set("")
        self.deskripsi_text.delete(1.0, END)
        
        # Clear treeview selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        
        self.status_label.config(text="Form telah direset", fg="orange")