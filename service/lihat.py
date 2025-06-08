from tkinter import *
from tkinter import ttk, messagebox
from database import DatabaseManager

class PageLihatTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Lihat Transaksi")
        self.root.geometry("900x600")
        self.root.configure(bg="#F1F1F1")
        
        self.db = DatabaseManager()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Title
        title_label = Label(self.root, text="Daftar Transaksi", font=("Arial", 16, "bold"), 
                           bg="#F1F1F1", fg="#333")
        title_label.pack(pady=15)
        
        # Info label
        self.info_label = Label(self.root, text="", font=("Arial", 10), 
                               bg="#F1F1F1", fg="#666")
        self.info_label.pack()
        
        # Main frame
        main_frame = Frame(self.root, bg="#F1F1F1")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Treeview dengan style yang lebih baik
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 9))
        
        # Treeview
        columns = ("ID", "Jenis", "Kategori", "Jumlah", "Tanggal", "Deskripsi")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=18)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Jenis", text="Jenis")
        self.tree.heading("Kategori", text="Kategori")
        self.tree.heading("Jumlah", text="Jumlah (Rp)")
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.heading("Deskripsi", text="Deskripsi")
        
        # Set column widths
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Jenis", width=100, anchor="center")
        self.tree.column("Kategori", width=120)
        self.tree.column("Jumlah", width=120, anchor="e")
        self.tree.column("Tanggal", width=100, anchor="center")
        self.tree.column("Deskripsi", width=200)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout untuk treeview dan scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Button frame
        btn_frame = Frame(self.root, bg="#F1F1F1")
        btn_frame.pack(pady=15)
        
        # Buttons
        Button(btn_frame, text="🔄 Refresh", command=self.load_data, 
               bg="#2196F3", fg="white", font=("Arial", 10), 
               padx=20, pady=5).pack(side="left", padx=5)
        
        Button(btn_frame, text="📊 Ringkasan", command=self.show_summary, 
               bg="#4CAF50", fg="white", font=("Arial", 10), 
               padx=20, pady=5).pack(side="left", padx=5)
        
        Button(btn_frame, text="❌ Tutup", command=self.root.destroy, 
               bg="#f44336", fg="white", font=("Arial", 10), 
               padx=20, pady=5).pack(side="left", padx=5)
    
    def load_data(self):
        try:
            # Clear existing data
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Load new data
            transaksi_list = self.db.get_all_transaksi()
            
            if not transaksi_list:
                self.info_label.config(text="Tidak ada data transaksi", fg="red")
                return
            
            # Insert data with formatting
            for transaksi in transaksi_list:
                # Format jumlah dengan separator ribuan
                jumlah_formatted = f"{transaksi[3]:,.0f}"
                
                # Buat tuple baru dengan format yang benar
                formatted_row = (
                    transaksi[0],  # ID
                    transaksi[1],  # Jenis
                    transaksi[2],  # Kategori
                    jumlah_formatted,  # Jumlah (formatted)
                    transaksi[4],  # Tanggal
                    transaksi[5] if transaksi[5] else "-"  # Deskripsi
                )
                
                # Insert dengan tag berdasarkan jenis transaksi
                if transaksi[1] == "Pemasukan":
                    self.tree.insert("", "end", values=formatted_row, tags=("pemasukan",))
                else:
                    self.tree.insert("", "end", values=formatted_row, tags=("pengeluaran",))
            
            # Configure tags untuk warna
            self.tree.tag_configure("pemasukan", foreground="green")
            self.tree.tag_configure("pengeluaran", foreground="red")
            
            # Update info
            total_rows = len(transaksi_list)
            self.info_label.config(text=f"Total: {total_rows} transaksi", fg="blue")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {str(e)}")
            self.info_label.config(text="Error memuat data", fg="red")
    
    def show_summary(self):
        try:
            laporan = self.db.get_laporan()
            
            summary_text = f"""
RINGKASAN KEUANGAN

Total Pemasukan: Rp {laporan['total_pemasukan']:,.0f}
Total Pengeluaran: Rp {laporan['total_pengeluaran']:,.0f}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Saldo Akhir: Rp {laporan['saldo']:,.0f}
            """
            
            messagebox.showinfo("Ringkasan Keuangan", summary_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menampilkan ringkasan: {str(e)}")