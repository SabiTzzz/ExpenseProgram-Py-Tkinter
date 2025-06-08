from tkinter import Toplevel, Label, Entry, Button

class PageHapusTransaksi:
    def __init__(self, root):
        self.root = root
        self.root.title("Hapus Transaksi")
        self.root.geometry("300x200")

        Label(root, text="ID Transaksi yang akan dihapus:").pack()
        self.id_entry = Entry(root)
        self.id_entry.pack()

        Button(root, text="Hapus", command=self.hapus).pack(pady=10)

    def hapus(self):
        transaksi_id = self.id_entry.get()
        print(f"Transaksi dengan ID {transaksi_id} dihapus.")
        self.root.destroy()
