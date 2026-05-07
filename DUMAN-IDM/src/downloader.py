import requests
import os
import time

# OOP: Temel Sınıf (Inheritance için)
class IndirmeAraci:
    def __init__(self, url):
        self.url = url
        self._durum = "Hazır" # Protected üye

# OOP: Kalıtım (IndirmeAraci'ndan miras alıyor)
class DosyaIndirici(IndirmeAraci):
    def __init__(self, url, kayit_yolu):
        super().__init__(url)
        self.kayit_yolu = kayit_yolu
        self.__indirilen_bayt = 0  # OOP: Encapsulation (Private üye)
        self.toplam_boyut = 0

    def indir(self, ilerleme_callback):
        try: # Hata Yönetimi
            headers = {"User-Agent": "Mozilla/5.0"}
            if os.path.exists(self.kayit_yolu):
                self.__indirilen_bayt = os.path.getsize(self.kayit_yolu)
                headers["Range"] = f"bytes={self.__indirilen_bayt}-"

            yanit = requests.get(self.url, stream=True, headers=headers, timeout=10)
            uzunluk = yanit.headers.get('content-length')
            if uzunluk:
                self.toplam_boyut = int(uzunluk) + self.__indirilen_bayt

            with open(self.kayit_yolu, "ab" if self.__indirilen_bayt > 0 else "wb") as f:
                baslangic = time.time()
                for parca in yanit.iter_content(chunk_size=32768):
                    if parca:
                        f.write(parca)
                        self.__indirilen_bayt += len(parca)
                        if self.toplam_boyut > 0:
                            yuzde = (self.__indirilen_bayt / self.toplam_boyut) * 100
                            ilerleme_callback(yuzde, 0)
            return True
        except Exception as e:
            print(f"Hata: {e}")
            return False