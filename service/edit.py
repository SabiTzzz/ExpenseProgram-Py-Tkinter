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
        # Title
        # title_label = Label(self.root, text="Edit Transaksi", font=("Arial", 16, "bold"), 
        #                    bg="#F1F1F1", fg="#333")
        # title_label.pack(pady=15)
        
        # # Main container
        # main_frame = Frame(self.root, bg="#F1F1F1")
        # main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # # Left side - List of transactions
        # left_frame = LabelFrame(main_frame, text="Pilih Transaksi", font=("Arial", 12, "bold"),
        #                        bg="#F1F1F1", fg="#333", padx=10, pady=10)
        # left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # # Treeview untuk daftar transaksi
        # columns = ("ID", "Jenis", "Kategori", "Jumlah", "Tanggal")
        # self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        
        # # Configure columns
        # self.tree.heading("ID", text="ID")
        # self.tree.heading("Jenis", text="Jenis")
        # self.tree.heading("Kategori", text="Kategori")
        # self.tree.heading("Jumlah", text="Jumlah")
        # self.tree.heading("Tanggal", text="Tanggal")
        
        # self.tree.column("ID", width=40, anchor="center")
        # self.tree.column("Jenis", width=80, anchor="center")
        # self.tree.column("Kategori", width=100)
        # self.tree.column("Jumlah", width=100, anchor="e")
        # self.tree.column("Tanggal", width=90, anchor="center")
        
        # # Scrollbar untuk treeview
        # tree_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        # self.tree.configure(yscrollcommand=tree_scroll.set)
        
        # self.tree.pack(side="left", fill="both", expand=True)
        # tree_scroll.pack(side="right", fill="y")
        
        # # Bind selection event
        # self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # # Right side - Edit form
        # right_frame = LabelFrame(main_frame, text="Form Edit", font=("Arial", 12, "bold"),
        #                         bg="#F1F1F1", fg="#333", padx=15, pady=15)
        # right_frame.pack(side="right", fill="y", padx=(10, 0))
        
        # # Form fields
        # # ID (readonly)
        # Label(right_frame, text="ID Transaksi:", bg="#F1F1F1", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        # self.id_var = StringVar()
        # id_entry = Entry(right_frame, textvariable=self.id_var, state="readonly", width=25)
        # id_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # # Jenis Transaksi
        # Label(right_frame, text="Jenis:", bg="#F1F1F1", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        # self.jenis_var = StringVar()
        # jenis_combo = ttk.Combobox(right_frame, textvariable=self.jenis_var, 
        #                            values=["Pemasukan", "Pengeluaran"], state="readonly", width=23)
        # jenis_combo.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # # Kategori
        # Label(right_frame, text="Kategori:", bg="#F1F1F1", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        # self.kategori_var = StringVar()
        # kategori_entry = Entry(right_frame, textvariable=self.kategori_var, width=25)
        # kategori_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # # Jumlah
        # Label(right_frame, text="Jumlah:", bg="#F1F1F1", font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        # self.jumlah_var = StringVar()
        # jumlah_entry = Entry(right_frame, textvariable=self.jumlah_var, width=25)
        # jumlah_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # # Tanggal
        # Label(right_frame, text="Tanggal:", bg="#F1F1F1", font=("Arial", 10)).grid(row=4, column=0, sticky="w", pady=5)
        # self.tanggal_var = StringVar()
        # tanggal_entry = Entry(right_frame, textvariable=self.tanggal_var, width=25)
        # tanggal_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # # Deskripsi
        # Label(right_frame, text="Deskripsi:", bg="#F1F1F1", font=("Arial", 10)).grid(row=5, column=0, sticky="nw", pady=5)
        # self.deskripsi_text = Text(right_frame, height=4, width=25)
        # self.deskripsi_text.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # # Buttons
        # btn_frame = Frame(right_frame, bg="#F1F1F1")
        # btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Button(btn_frame, text="🔄 Refresh List", command=self.load_transaksi_list, 
        #        bg="#2196F3", fg="white", font=("Arial", 9), padx=10).pack(side="top", fill="x", pady=2)
        
        # Button(btn_frame, text="💾 Simpan Perubahan", command=self.simpan_perubahan, 
        #        bg="#4CAF50", fg="white", font=("Arial", 9), padx=10).pack(side="top", fill="x", pady=2)
        
        # Button(btn_frame, text="🔄 Reset Form", command=self.reset_form, 
        #        bg="#FF9800", fg="white", font=("Arial", 9), padx=10).pack(side="top", fill="x", pady=2)
        
        # Button(btn_frame, text="❌ Tutup", command=self.root.destroy, 
        #        bg="#f44336", fg="white", font=("Arial", 9), padx=10).pack(side="top", fill="x", pady=2)
        
        # # Configure grid weights
        # right_frame.columnconfigure(1, weight=1)
        
        # # Status label
        # self.status_label = Label(self.root, text="Pilih transaksi dari daftar untuk mengedit", 
        #                          font=("Arial", 10), bg="#F1F1F1", fg="#666")
        # self.status_label.pack(pady=10)
    
    def form_edit_transaksi(self):
        print("Form Edit Transaksi")

    def load_transaksi_list(self):
        try:
            # Clear existing data
            # for item in self.tree.get_children():
            #     self.tree.delete(item)
            
            # Load data from database
            transaksi_list = self.db.get_all_transaksi()
            
            if not transaksi_list:
                # self.status_label.config(text="Tidak ada data transaksi", fg="red")
                return
            
            self.bgPanel = []
            self.bgIndex = []
            # Insert data into treeview
            jarak = 0
            i = 0
            for transaksi in transaksi_list:
                if len(transaksi) == 1:
                    self.bgPanel.append(PhotoImage(file=relative_to_assets("Panel.png")))
                    self.bgPanel_frame = self.canvas.create_image(220, 230, image=self.bgPanel[i])

                    self.bgIndex.append(PhotoImage(file=relative_to_assets("Circle.png")))
                    self.bgIndex_frame = self.canvas.create_image(0, 0, image=self.bgIndex[i])

                    self.canvas.create_line(60, 163, 380, 163, fill="#000000", width=1)
                    Label(self.root, text=f"{transaksi[0]}", bg="#FFFFFF", font=("Arial", 12)).place(x=15, y=160)
                    Label(self.root, text=f"Jenis: {transaksi[1]}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=170)
                    Label(self.root, text=f"Kategori: {transaksi[2]}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=193)
                    Label(self.root, text=f"Jumlah: {transaksi[3]:,.0f}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=216)
                    Label(self.root, text=f"Tanggal: {transaksi[4]}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=239)
                    Label(self.root, text=f"Deskripsi: {transaksi[5] if transaksi[5] else 'Tidak ada'}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=262)
                    self.canvas.create_line(60, 290, 380, 290, fill="#000000", width=1)
                    i += 1
                    jarak += 170
                else:
                    self.bgPanel.append(PhotoImage(file=relative_to_assets("Panel.png")))
                    self.bgPanel_frame = self.canvas.create_image(220, 230 + jarak + 10, image=self.bgPanel[i])

                    self.canvas.create_line(60, 163 + jarak + 10, 380, 163 + jarak + 10, fill="#000000", width=1)
                    Label(self.root, text=f"{transaksi[0]}", bg="#FFFFFF", font=("Arial", 12)).place(x=15, y=160 + jarak + 10)
                    Label(self.root, text=f"Jenis: {transaksi[1]}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=170 + jarak + 10)
                    Label(self.root, text=f"Kategori: {transaksi[2]}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=193 + jarak + 10)
                    Label(self.root, text=f"Jumlah: {transaksi[3]:,.0f}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=216 + jarak + 10)
                    Label(self.root, text=f"Tanggal: {transaksi[4]}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=239 + jarak + 10)
                    Label(self.root, text=f"Deskripsi: {transaksi[5] if transaksi[5] else 'Tidak ada'}", bg="#FFFFFF", font=("Arial", 11)).place(x=60, y=262 + jarak + 10)
                    self.canvas.create_line(60, 290 + jarak + 10, 380, 290 + jarak + 10, fill="#000000", width=1)
                    i += 1
                    jarak += 170

                # jumlah_formatted = f"{transaksi[3]:,.0f}"
                # formatted_row = (
                #     transaksi[0],  # ID
                #     transaksi[1],  # Jenis
                #     transaksi[2],  # Kategori
                #     jumlah_formatted,  # Jumlah
                #     transaksi[4],  # Tanggal
                # )
                
                # if transaksi[1] == "Pemasukan":
                #     self.tree.insert("", "end", values=formatted_row, tags=("pemasukan",))
                # else:
                #     self.tree.insert("", "end", values=formatted_row, tags=("pengeluaran",))
            
            # Configure tags
            # self.tree.tag_configure("pemasukan", foreground="green")
            # self.tree.tag_configure("pengeluaran", foreground="red")
            
            # self.status_label.config(text=f"Loaded {len(transaksi_list)} transaksi", fg="blue")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")
            # self.status_label.config(text="Error memuat data", fg="red")
    
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
                self.selected_id = transaksi[0]
                
                # Fill form fields
                self.id_var.set(str(transaksi[0]))
                self.jenis_var.set(transaksi[1])
                self.kategori_var.set(transaksi[2])
                self.jumlah_var.set(str(transaksi[3]))
                self.tanggal_var.set(transaksi[4])
                
                # Clear and set description
                self.deskripsi_text.delete(1.0, END)
                if transaksi[5]:
                    self.deskripsi_text.insert(1.0, transaksi[5])
                
                self.status_label.config(text=f"Editing transaksi ID: {transaksi[0]}", fg="blue")
            
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