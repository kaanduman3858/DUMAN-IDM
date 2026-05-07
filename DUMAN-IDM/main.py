import tkinter as tk
from tkinter import filedialog, ttk
import threading
import os
from src.downloader import DosyaIndirici # Modüler bağlantı
from queue import Queue

class DumanIDM(tk.Tk): 
    def __init__(self):
        super().__init__()
        self.title("Duman IDM - Modüler Sürüm")
        self.geometry("900x600")
        self.configure(bg="#12121c")
        self.kuyruk = Queue()
        self.arayuz_ciz()
        threading.Thread(target=self.isleyici, daemon=True).start()

    def arayuz_ciz(self):
        # Üst Panel
        ust = tk.Frame(self, bg="#12121c", pady=20)
        ust.pack(fill="x", padx=30)
        self.url_ent = tk.Entry(ust, bg="#1a1a2e", fg="white", font=("Segoe UI", 12), relief="flat")
        self.url_ent.pack(side="left", fill="x", expand=True, ipady=10, padx=10)
        tk.Button(ust, text="EKLE", command=self.ekle, bg="#9d4edd", fg="white", padx=25).pack(side="right")
        # Liste
        self.liste_frame = tk.Frame(self, bg="#12121c")
        self.liste_frame.pack(fill="both", expand=True, padx=30)

    def ekle(self):
        url = self.url_ent.get().strip()
        if url:
            yol = filedialog.asksaveasfilename(initialfile=(url.split("/")[-1] or "dosya.bin"))
            if yol:
                oge = DosyaIndirici(url, yol)
                self.kart_ekle(oge)
                self.kuyruk.put(oge)
                self.url_ent.delete(0, tk.END)

    def kart_ekle(self, oge):
        kart = tk.Frame(self.liste_frame, bg="#24243e", pady=15, padx=20)
        kart.pack(fill="x", pady=10)
        tk.Label(kart, text=os.path.basename(oge.kayit_yolu), fg="white", bg="#24243e").pack(side="left")
        oge.pb = ttk.Progressbar(kart, length=300, mode='determinate')
        oge.pb.pack(side="right", padx=20)

    def isleyici(self):
        while True:
            oge = self.kuyruk.get()
            oge.indir(lambda y, h: self.guncelle(oge, y))
            self.kuyruk.task_done()

    def guncelle(self, oge, y):
        oge.pb.config(value=y)
        self.update_idletasks()

if __name__ == "__main__":
    app = DumanIDM()
    app.mainloop()