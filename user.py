from transaction import Transaction
from datetime import datetime,timedelta


class User:
    def __init__(self, isim):
        self.isim = isim
        self.transactions = []

    def __str__(self):
        return f"Hoşgeldin {self.isim}!"

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def gider_kayit(self):
        aylik_gider_sayisi = int(input("kaç adet aylık gideriniz var?: "))
        for x in range(aylik_gider_sayisi):
            miktar = int(input(f"{x+1}. gider miktarı: "))
            kategori = "net_gider"
            gun = int(input(f"{x+1}. giderin gelme günü (1,15...): "))
            tarih = datetime(datetime.now().year, datetime.now().month, gun)
            t1 = Transaction(kategori, miktar, gun, "gider", tarih)
            self.add_transaction(t1)

    def gelir_kayit(self):
        aylik_gelir_sayisi = int(input("kaç adet aylık geliriniz var?: "))
        for x in range(aylik_gelir_sayisi):
            miktar = int(input(f"{x+1}. gelir miktarı: "))
            kategori = "net_gelir"
            gun = int(input(f"{x+1}. gelirin gelme günü (1,15...): "))
            tarih = datetime(datetime.now().year, datetime.now().month, gun)
            t1 = Transaction(kategori, miktar, gun, "gelir", tarih)
            self.add_transaction(t1)

    def gelir_gider_hesapla(self):
        self.net_gelir = sum(
            (
                t.miktar
                for t in self.transactions
                if t.tur == "gelir" and t.kategori == "net_gelir"
            )
        )
        self.net_gider = sum(
            (
                t.miktar
                for t in self.transactions
                if t.tur == "gider" and t.kategori == "net_gider"
            )
        )
        self.aylik_gider=sum(
            (
                t.miktar
                for t in self.transactions
                if t.tur=="gider" and t.kategori=="gunluk_gider" and t.tarih>datetime.now().date()-timedelta(days=30)
            )
        )
        self.net_kalan = self.net_gelir - self.net_gider
        self.aylik_kalan = self.net_kalan-self.aylik_gider
        print(f"kalan para: {self.aylik_kalan}")
    def gunluk_gider(self):
        gunluk_gider_sayisi = int(input("bugün kaç adet harcama yaptınız:"))
        for x in range(gunluk_gider_sayisi):
            miktar = int(input(f"{x+1}. gider miktarı "))
            tarih = datetime.now().date()
            t1 = Transaction("gunluk_gider", miktar, tarih.day, "gider", tarih)
            self.add_transaction(t1)
        print(f"{gunluk_gider_sayisi} adet gider kaydedildi.")
        toplam = sum(t.miktar for t in self.transactions if t.kategori == "gunluk_gider" and t.tarih == datetime.now().date())
        if toplam > (self.net_kalan/30):
            print("bugünkü gider olması gerekenden yüksek")
        else:
            print(f"bugün kalan gider limitiniz: {(self.net_kalan/30)-toplam}")
    def ek_gelir(self,miktar):
        t1 = Transaction("ek_gelir",miktar,datetime.now().date().day,"gelir",datetime.now().date())
        self.add_transaction(t1)
        print(f"{miktar} TL ek gelir eklendi")