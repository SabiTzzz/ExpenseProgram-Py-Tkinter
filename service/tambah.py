from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from database import DatabaseManager

class PageTambahTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tambah Transaksi")
        self.root.geometry("400x400")
        self.root.configure(bg="#F1F1F1")
        self.root.resizable(False, False)
        
        self.db = DatabaseManager()
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        Label(self.root, text="Tambah Transaksi", font=("Arial", 16, "bold"), 
              bg="#F1F1F1").pack(pady=10)
        
        # Frame untuk form
        frame = Frame(self.root, bg="#F1F1F1")
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Jenis Transaksi
        Label(frame, text="Jenis:", bg="#F1F1F1").grid(row=0, column=0, sticky="w", pady=5)
        self.jenis_var = StringVar(value="Pemasukan")
        jenis_combo = ttk.Combobox(frame, textvariable=self.jenis_var, 
                                   values=["Pemasukan", "Pengeluaran"], state="readonly")
        jenis_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Kategori
        Label(frame, text="Kategori:", bg="#F1F1F1").grid(row=1, column=0, sticky="w", pady=5)
        self.kategori_entry = Entry(frame)
        self.kategori_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Jumlah
        Label(frame, text="Jumlah:", bg="#F1F1F1").grid(row=2, column=0, sticky="w", pady=5)
        self.jumlah_entry = Entry(frame)
        self.jumlah_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Tanggal
        Label(frame, text="Tanggal:", bg="#F1F1F1").grid(row=3, column=0, sticky="w", pady=5)
        self.tanggal_entry = Entry(frame)
        self.tanggal_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.tanggal_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Deskripsi
        Label(frame, text="Deskripsi:", bg="#F1F1F1").grid(row=4, column=0, sticky="nw", pady=5)
        self.deskripsi_text = Text(frame, height=3)
        self.deskripsi_text.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = Frame(frame, bg="#F1F1F1")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        Button(btn_frame, text="Simpan", command=self.simpan_transaksi, 
               bg="#4CAF50", fg="white", width=10).pack(side="left", padx=5)
        Button(btn_frame, text="Batal", command=self.root.destroy, 
               bg="#f44336", fg="white", width=10).pack(side="left", padx=5)
        
        # Configure grid weights
        frame.columnconfigure(1, weight=1)
    
    def simpan_transaksi(self):
        try:
            jenis = self.jenis_var.get()
            kategori = self.kategori_entry.get().strip()
            jumlah = float(self.jumlah_entry.get())
            tanggal = self.tanggal_entry.get().strip()
            deskripsi = self.deskripsi_text.get(1.0, END).strip()
            
            if not kategori:
                messagebox.showerror("Error", "Kategori harus diisi!")
                return
            
            self.db.tambah_transaksi(jenis, kategori, jumlah, tanggal, deskripsi)
            messagebox.showinfo("Sukses", "Transaksi berhasil ditambahkan!")
            self.root.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")