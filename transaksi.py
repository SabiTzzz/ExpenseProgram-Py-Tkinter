from datetime import datetime

class Transaksi:
    def __init__(self, id_transaksi, jenis, kategori, jumlah, tanggal, deskripsi):
        self.id_transaksi = id_transaksi
        self.jenis = jenis
        self.kategori = kategori
        self.jumlah = jumlah
        self.tanggal = tanggal
        self.deskripsi = deskripsi

    def __str__(self):
        return (f"ID: {self.id_transaksi}, Jenis: {self.jenis}, Kategori: {self.kategori}, "
                f"Jumlah: {self.jumlah}, Tanggal: {self.tanggal}, Deskripsi: {self.deskripsi}")