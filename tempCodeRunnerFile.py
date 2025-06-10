class Transaksi:
    def __init__(self, id_transaksi, kategori, jumlah, tanggal, deskripsi):
        self.id_transaksi = id_transaksi
        self.kategori = kategori
        self.jumlah = jumlah
        self.tanggal = tanggal
        self.deskripsi = deskripsi
    
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