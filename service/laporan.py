from tkinter import *
from database import DatabaseManager

class PageLaporan:
    def __init__(self, root):
        self.root = root
        self.root.title("Laporan Keuangan")
        self.root.geometry("400x300")
        self.root.configure(bg="#F1F1F1")
        
        self.db = DatabaseManager()
        self.setup_ui()
        self.load_laporan()
    
    def setup_ui(self):
        # Title
        Label(self.root, text="Laporan Keuangan", font=("Arial", 18, "bold"), 
              bg="#F1F1F1").pack(pady=20)
        
        # Frame untuk laporan
        frame = Frame(self.root, bg="white", relief="raised", bd=2)
        frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Labels untuk menampilkan data
        self.pemasukan_label = Label(frame, text="Total Pemasukan: Rp 0", 
                                    font=("Arial", 12), bg="white", fg="green")
        self.pemasukan_label.pack(pady=10)
        
        self.pengeluaran_label = Label(frame, text="Total Pengeluaran: Rp 0", 
                                      font=("Arial", 12), bg="white", fg="red")
        self.pengeluaran_label.pack(pady=10)
        
        self.saldo_label = Label(frame, text="Saldo: Rp 0", 
                                font=("Arial", 14, "bold"), bg="white")
        self.saldo_label.pack(pady=15)
        
        # Button refresh
        Button(self.root, text="Refresh Laporan", command=self.load_laporan, 
               bg="#2196F3", fg="white", width=15).pack(pady=10)
    
    def load_laporan(self):
        laporan = self.db.get_laporan()
        
        self.pemasukan_label.config(text=f"Total Pemasukan: Rp {laporan['total_pemasukan']:,.0f}")
        self.pengeluaran_label.config(text=f"Total Pengeluaran: Rp {laporan['total_pengeluaran']:,.0f}")
        
        saldo = laporan['saldo']
        color = "green" if saldo >= 0 else "red"
        self.saldo_label.config(text=f"Saldo: Rp {saldo:,.0f}", fg=color)