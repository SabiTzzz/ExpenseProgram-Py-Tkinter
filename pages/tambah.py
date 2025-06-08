from tkinter import Toplevel, Label, Entry, Button

class PageTambahTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tambah Transaksi")
        self.root.geometry("300x300")

        Label(root, text="Nama Transaksi:").pack()
        self.nama_entry = Entry(root)
        self.nama_entry.pack()

        Label(root, text="Jumlah:").pack()
        self.jumlah_entry = Entry(root)
        self.jumlah_entry.pack()

        Button(root, text="Simpan", command=self.simpan).pack(pady=10)

    def simpan(self):
        nama = self.nama_entry.get()
        jumlah = self.jumlah_entry.get()
        print(f"Transaksi disimpan: {nama}, jumlah: {jumlah}")
        self.root.destroy()
