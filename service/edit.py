from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from database import DatabaseManager

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
        Button(self.root, image=self.button_ubahId, borderwidth=0, bg="#369394", command=self.form_edit_transaksi, relief="flat", highlightthickness=0).place(x=280.0, y=670.0, width=103.0, height=45.0)

        self.bgtxt_id = PhotoImage(file=relative_to_assets("Textbox.png"))
        self.txt_id_frame = self.canvas.create_image(120.0, 695.0, image=self.bgtxt_id)
        Entry(self.canvas, font=("Arial", 12), width=20, relief="flat").place(x=45, y=677.0, width=150, height=26)

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

        # Info Label
        self.info_label = Label(self.root, text="", font=("Arial", 10), bg="#FFFFFF", fg="#666")
        self.info_label.place(x=10, y=710)
    
    def form_edit_transaksi(self):
        try:
            # Get ID from entry
            id_entry = self.canvas.find_withtag("current")
            id_value = self.canvas.itemcget(id_entry, "text").strip()
            
            if not id_value.isdigit():
                messagebox.showerror("Error", "ID harus berupa angka!")
                return
            
            transaksi_id = int(id_value)
            
            self.canvas_e = Canvas(
                self.root,
                bg="#FFFFFF",
                height=752,
                width=412,
                bd=0,
                highlightthickness=0,
                relief="ridge"
            )
            self.canvas_e.place(x=0, y=0)

            self.image_edit = PhotoImage(file=relative_to_assets("EditForm.png"))
            self.canvas_e.create_image(206.0, 376.0, image=self.image_edit)

            # Tombol Kembali
            self.btn_kembali_edit = PhotoImage(file=relative_to_assets("btnKembali.png"))
            Button(
                self.root,
                image=self.btn_kembali_edit,
                borderwidth=0,
                highlightthickness=0,
                command=self.root.destroy,
                relief="flat"
            ).place(x=13.0, y=35.0, width=100.0, height=22.188)

            # Tombol Simpan Perubahan
            self.btn_simpan_edit = PhotoImage(file=relative_to_assets("btnSimpanEdit.png"))
            Button(
                self.root,
                image=self.btn_simpan_edit,
                borderwidth=0,
                highlightthickness=0,
                command=self.simpan_perubahan,
                relief="flat"
            ).place(x=86.0, y=692.0, width=108.0, height=30.0)

            # Tombol Batal
            self.btn_batal_edit = PhotoImage(file=relative_to_assets("btnBatalEdit.png"))
            Button(
                self.root,
                image=self.btn_batal_edit,
                borderwidth=0,
                highlightthickness=0,
                command=self.reset_form,
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

            # Variabel untuk menyimpan ID yang dipilih
            self.selected_id = transaksi_id
            self.status_label = Label(self.root, text="", font=("Arial", 10), bg="#FFFFFF", fg="#666")
            self.status_label.place(x=10, y=710)
            self.load_transaksi_detail(transaksi_id)
            self.load_transaksi_list()
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat detail transaksi: {str(e)}")

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