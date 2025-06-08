from tkinter import *
from tkinter import ttk
import sys
import os

# Tambahkan parent directory ke path untuk import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_page import BasePage
from database import DatabaseManager

class PageHapusTransaksi(BasePage):
    """Page untuk menghapus transaksi"""
    
    def __init__(self, root):
        self.db = DatabaseManager()
        super().__init__(root, "Hapus Transaksi", height=500)
    
    def setup_ui(self):
        # Header
        self.create_header("Hapus Transaksi")
        
        # Search area
        self.create_search_area()
        
        # Treeview untuk menampilkan data
        self.create_treeview()
        
        # Buttons
        self.create_buttons()
        
        # Load data
        self.load_data()
    
    def create_search_area(self):
        """Buat area pencarian"""
        search_frame = Frame(self.root, bg="#F1F1F1")
        search_frame.place(x=20, y=90, width=372, height=50)
        
        Label(search_frame, text="Cari Transaksi:", bg="#F1F1F1", font=("Arial", 10)).place(x=0, y=5)
        
        self.search_var = StringVar()
        search_entry = Entry(search_frame, textvariable=self.search_var, font=("Arial", 10), width=25)
        search_entry.place(x=0, y=25)
        
        search_btn = Button(
            search_frame,
            text="Cari",
            bg="#2196F3",
            fg="white",
            font=("Arial", 9),
            borderwidth=0,
            cursor="hand2",
            command=self.search_transaksi
        )
        search_btn.place(x=200, y=23, width=50, height=25)
        
        reset_btn = Button(
            search_frame,
            text="Reset",
            bg="#FF9800",
            fg="white",
            font=("Arial", 9),
            borderwidth=0,
            cursor="hand2",
            command=self.reset_search
        )
        reset_btn.place(x=255, y=23, width=50, height=25)
    
    def create_treeview(self):
        """Buat treeview untuk menampilkan data"""
        # Frame untuk treeview dan scrollbar
        tree_frame = Frame(self.root)
        tree_frame.place(x=20, y=150, width=372, height=280)
        
        # Treeview
        columns = ('ID', 'Jenis', 'Kategori', 'Jumlah', 'Tanggal')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Jenis', text='Jenis')
        self.tree.heading('Kategori', text='Kategori')
        self.tree.heading('Jumlah', text='Jumlah')
        self.tree.heading('Tanggal', text='Tanggal')
        
        # Define column widths
        self.tree.column('ID', width=40, anchor=CENTER)
        self.tree.column('Jenis', width=80, anchor=CENTER)
        self.tree.column('Kategori', width=80, anchor=CENTER)
        self.tree.column('Jumlah', width=100, anchor=E)
        self.tree.column('Tanggal', width=80, anchor=CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview dan scrollbar
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
    
    def create_buttons(self):
        """Buat tombol-tombol"""
        button_y = 440
        
        # Selected info
        self.selected_label = Label(
            self.root,
            text="Belum ada transaksi yang dipilih",
            bg="#F1F1F1",
            font=("Arial", 10),
            fg="gray"
        )
        self.selected_label.place(x=20, y=button_y - 25)
        
        # Hapus Button
        self.hapus_btn = Button(
            self.root,
            text="Hapus Transaksi",
            bg="#F44336",
            fg="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            cursor="hand2",
            command=self.hapus_transaksi,
            state=DISABLED
        )
        self.hapus_btn.place(x=20, y=button_y, width=150, height=40)
        
        # Refresh Button
        refresh_btn = Button(
            self.root,
            text="Refresh",
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            cursor="hand2",
            command=self.load_data
        )
        refresh_btn.place(x=180, y=button_y, width=100, height=40)
        
        # Detail Button
        self.detail_btn = Button(
            self.root,
            text="Detail",
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            cursor="hand2",
            command=self.show_detail,
            state=DISABLED
        )
        self.detail_btn.place(x=290, y=button_y, width=100, height=40)
    
    def load_data(self):
        """Load data transaksi ke treeview"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load data dari database
        try:
            transaksi_list = self.db.get_all_transaksi()
            
            for transaksi in transaksi_list:
                # Format jumlah
                jumlah_text = self.format_currency(abs(transaksi.jumlah))
                
                self.tree.insert('', 'end', values=(
                    transaksi.id_transaksi,
                    transaksi.get_jenis(),
                    transaksi.kategori,
                    jumlah_text,
                    transaksi.tanggal
                ))
            
        except Exception as e:
            self.show_error_message(f"Error loading data: {str(e)}")
    
    def search_transaksi(self):
        """Cari transaksi berdasarkan keyword"""
        keyword = self.search_var.get().strip().lower()
        
        if not keyword:
            self.load_data()
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load dan filter data
        try:
            transaksi_list = self.db.get_all_transaksi()
            
            for transaksi in transaksi_list:
                # Cek apakah keyword ada di salah satu field
                if (keyword in str(transaksi.id_transaksi).lower() or
                    keyword in transaksi.get_jenis().lower() or
                    keyword in transaksi.kategori.lower() or
                    keyword in str(transaksi.tanggal).lower() or
                    keyword in (transaksi.deskripsi or "").lower()):
                    
                    jumlah_text = self.format_currency(abs(transaksi.jumlah))
                    
                    self.tree.insert('', 'end', values=(
                        transaksi.id_transaksi,
                        transaksi.get_jenis(),
                        transaksi.kategori,
                        jumlah_text,
                        transaksi.tanggal
                    ))
            
        except Exception as e:
            self.show_error_message(f"Error searching data: {str(e)}")
    
    def reset_search(self):
        """Reset pencarian"""
        self.search_var.set("")
        self.load_data()
    
    def on_select(self, event):
        """Handle selection change"""
        selection = self.tree.selection()
        
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            
            # Update label
            self.selected_label.config(
                text=f"Dipilih: ID {values[0]} - {values[1]} - {values[2]}",
                fg="black"
            )
            
            # Enable buttons
            self.hapus_btn.config(state=NORMAL)
            self.detail_btn.config(state=NORMAL)
        else:
            # Reset label
            self.selected_label.config(
                text="Belum ada transaksi yang dipilih",
                fg="gray"
            )
            
            # Disable buttons
            self.hapus_btn.config(state=DISABLED)
            self.detail_btn.config(state=DISABLED)
    
    def get_selected_item(self):
        """Dapatkan item yang dipilih"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            return item['values']
        return None
    
    def show_detail(self):
        """Tampilkan detail transaksi yang dipilih"""
        selected_item = self.get_selected_item()
        
        if not selected_item:
            self.show_warning_message("Silakan pilih transaksi terlebih dahulu!")
            return
        
        id_transaksi = selected_item[0]
        transaksi = self.db.get_transaksi_by_id(id_transaksi)
        
        if not transaksi:
            self.show_warning_message("Transaksi tidak ditemukan!")
            return