import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="keuangan.db"):
        self.db_name = db_name
        self.setup_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def setup_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jenis TEXT NOT NULL,
                kategori TEXT NOT NULL,
                jumlah REAL NOT NULL,
                tanggal TEXT NOT NULL,
                deskripsi TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def tambah_transaksi(self, jenis, kategori, jumlah, tanggal, deskripsi):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transaksi (jenis, kategori, jumlah, tanggal, deskripsi)
            VALUES (?, ?, ?, ?, ?)
        ''', (jenis, kategori, jumlah, tanggal, deskripsi))
        
        conn.commit()
        conn.close()
    
    def get_all_transaksi(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM transaksi ORDER BY tanggal DESC')
        rows = cursor.fetchall()
        
        conn.close()
        return rows
    
    def cek_id_transaksi(self, id_transaksi):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM transaksi WHERE id = ?', (id_transaksi,))
        exists = cursor.fetchone() is not None
        
        conn.close()
        return exists
    
    def hapus_transaksi(self, id_transaksi):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transaksi WHERE id = ?', (id_transaksi,))
        
        conn.commit()
        conn.close()
    
    def update_transaksi(self, id_transaksi, jenis, kategori, jumlah, tanggal, deskripsi):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE transaksi 
            SET jenis=?, kategori=?, jumlah=?, tanggal=?, deskripsi=?
            WHERE id=?
        ''', (jenis, kategori, jumlah, tanggal, deskripsi, id_transaksi))
        
        conn.commit()
        conn.close()
    
    def get_laporan(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total pemasukan
        cursor.execute('SELECT SUM(jumlah) FROM transaksi WHERE jenis = "Pemasukan"')
        total_pemasukan = cursor.fetchone()[0] or 0
        
        # Total pengeluaran
        cursor.execute('SELECT SUM(jumlah) FROM transaksi WHERE jenis = "Pengeluaran"')
        total_pengeluaran = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_pemasukan': total_pemasukan,
            'total_pengeluaran': total_pengeluaran,
            'saldo': total_pemasukan - total_pengeluaran
        }

    def get_pengeluaran_by_kategori(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT kategori, SUM(jumlah) AS total
            FROM transaksi
            WHERE jenis = 'Pengeluaran'
            GROUP BY kategori
        """)
        return cursor.fetchall()