from tkinter import *
from tkinter import messagebox, ttk
from database import DatabaseManager

class PageHapusTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Hapus Transaksi")
        self.root.geometry("600x400")
        self.root.configure(bg="#F1F1F1")
        
        self.db = DatabaseManager()
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        # Title
        Label(self.root, text="Hapus Transaksi", font=("Arial", 16, "bold"), 
              bg="#F1F1F1").pack(pady=10)
        
        # Frame untuk treeview
        frame = Frame(self.root, bg="#F1F1F1")
        frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Treeview
        columns = ("ID", "Jenis", "Kategori", "Jumlah", "Tanggal")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Buttons
        btn_frame = Frame(self.root, bg="#F1F1F1")
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="Hapus", command=self.hapus_transaksi, 
               bg="#f44336", fg="white", width=10).pack(side="left", padx=5)
        Button(btn_frame, text="Refresh", command=self.load_data, 
               bg="#2196F3", fg="white", width=10).pack(side="left", padx=5)
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        transaksi_list = self.db.get_all_transaksi()
        for transaksi in transaksi_list:
            self.tree.insert("", "end", values=transaksi[:5])  # Tanpa deskripsi
    
    def hapus_transaksi(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Pilih transaksi yang akan dihapus!")
            return
        
        item = self.tree.item(selected[0])
        transaksi_id = item['values'][0]
        
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus transaksi ini?"):
            try:
                self.db.hapus_transaksi(transaksi_id)
                messagebox.showinfo("Sukses", "Transaksi berhasil dihapus!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus: {str(e)}")