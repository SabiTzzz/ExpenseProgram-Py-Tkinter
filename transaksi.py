class Transaksi:
    def __init__(self, id_transaksi, kategori, jumlah, tanggal, deskripsi):
        self.id_transaksi = id_transaksi
        self.kategori = kategori
        self.jumlah = jumlah
        self.tanggal = tanggal
        self.deskripsi = deskripsi
    
    def __str__(self):
        return (f"ID: {self.id_transaksi}, Jenis: {self.get_jenis()}, Kategori: {self.kategori}, "
                f"Jumlah: {self.jumlah}, Tanggal: {self.tanggal}, Deskripsi: {self.deskripsi}")
    
    def get_jenis(self):
        return "Unknown"

class Pemasukan(Transaksi):
    def __init__(self, id_transaksi, kategori, jumlah, tanggal, deskripsi):
        super().__init__(id_transaksi, kategori, jumlah, tanggal, deskripsi)
    
    def get_jenis(self):
        return "Pemasukan"

class Pengeluaran(Transaksi):
    def __init__(self, id_transaksi, kategori, jumlah, tanggal, deskripsi):
        super().__init__(id_transaksi, kategori, jumlah, tanggal, deskripsi)
    
    def get_jenis(self):
        return "Pengeluaran"