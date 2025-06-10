from tkinter import *
from pathlib import Path
from database import DatabaseManager
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PageLaporan:
    def __init__(self, window):
        self.window = window
        self.window.title("Laporan Keuangan")
        self.window.configure(bg="#F1F1F1")

        self.db = DatabaseManager()

        OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = OUTPUT_PATH.parent / Path(r"assets/frame0")

        def relative_to_assets(path: str) -> Path:
            return self.ASSETS_PATH / Path(path)

        self.relative_to_assets = relative_to_assets

        self.canvas = Canvas(
            self.window,
            bg="#F1F1F1",
            height=765,
            width=412,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("Laporan.png"))
        self.canvas.create_image(
            206,  # Tengah dari width 412
            382.5,
            image=self.image_image_1
        )

        # Tombol kembali
        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("btnKembali.png"))
        self.button_1 = Button(
            self.window,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.window.destroy,
            relief="flat"
        )
        self.button_1.place(
            x=13,
            y=35,
            width=100.0,
            height=22.188
        )

        # Label teks (disesuaikan dengan ukuran canvas)
        self.text_pengeluaran = self.canvas.create_text(
            20,
            600,
            anchor="nw",
            text="Total Pengeluaran\nRp xxx.xxx",
            fill="#FFFFFF",
            font=("Poppins Bold", 20 * -1)
        )

        self.text_pemasukan = self.canvas.create_text(
            20,
            670,
            anchor="nw",
            text="Total Pemasukan\nRp xxx.xxx",
            fill="#FFFFFF",
            font=("Poppins Bold", 20 * -1)
        )

        self.text_saldo = self.canvas.create_text(
            37,
            537,
            anchor="nw",
            text="Total Saldo : Rp xxx.xxx",
            fill="#FFFFFF",
            font=("Poppins Bold", 20 * -1)
        )

        # Load data & tampilkan grafik
        self.load_laporan()
        self.tampilkan_grafik_di_tkinter(self.canvas)

    def load_laporan(self):
        laporan = self.db.get_laporan()

        # Update label "Total Pemasukan"
        self.canvas.itemconfig(
            self.text_pemasukan,
            text="[ Total Pemasukan ]",
            font=("Poppins Bold", 20 * -1)
        )
        # Tambahkan jumlah uang pemasukan di bawahnya
        self.pemasukan_amount = self.canvas.create_text(
            20,
            700,
            anchor="nw",
            text=f"Rp {laporan['total_pemasukan']:,.0f}",
            fill="#FFFFFF",
            font=("Poppins", 18 * -1, "bold")
        )

        # Update label "Total Pengeluaran"
        self.canvas.itemconfig(
            self.text_pengeluaran,
            text="[ Total Pengeluaran ]",
            font=("Poppins Bold", 20 * -1)
        )
        # Tambahkan jumlah uang pengeluaran di bawahnya
        self.pengeluaran_amount = self.canvas.create_text(
            20,
            630,
            anchor="nw",
            text=f"Rp {laporan['total_pengeluaran']:,.0f}",
            fill="#FFFFFF",
            font=("Poppins", 18 * -1, "bold")
        )
        
        # Update label "Total Saldo"
        self.canvas.itemconfig(
            self.text_saldo,
            text="Total Saldo :",
            font=("Poppins Bold", 20 * -1)
        )
        # Tambahkan jumlah saldo di sampingnya
        self.saldo_amount = self.canvas.create_text(
            175,
            538,
            anchor="nw",
            text=f"Rp {laporan['saldo']:,.0f}",
            fill="#FFFFFF",
            font=("Poppins", 18 * -1, "bold")
        )

    def tampilkan_grafik_di_tkinter(self, parent_canvas):
        # Data dummy (ganti jika ingin dari database)
        data = self.db.get_pengeluaran_by_kategori()
        if not data:
            return

        labels, values = zip(*data)
        colors = ['#A8D0E6', '#F76C6C', '#C0F5C3', '#FFD700', '#FFA07A']

        self.grafik_frame = Frame(parent_canvas, bg="#F1F1F1", width=250, height=250)
        self.grafik_frame.pack_propagate(False)

        fig = Figure(figsize=(5, 5), dpi=100, facecolor="#F1F1F1")
        ax = fig.add_subplot(111, facecolor="#F1F1F1")
        wedges, texts, autotexts = ax.pie(
            values,
            colors=colors,
            autopct='%1.0f%%',
            startangle=90,
            textprops={'fontsize': 7}
        )
        for i, autotext in enumerate(autotexts):
            autotext.set_text(f"{labels[i]}\n{autotext.get_text()}")
        ax.axis('equal')
        ax.set_title("Persentase Pengeluaran", fontsize=9, fontweight='bold', backgroundcolor="#F1F1F1")

        chart_canvas = FigureCanvasTkAgg(fig, master=self.grafik_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(expand=True)

        # Tempatkan di tengah atas
        parent_canvas.create_window(76, 190, anchor="nw", window=self.grafik_frame)