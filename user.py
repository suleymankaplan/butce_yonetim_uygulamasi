from datetime import datetime,timedelta
from datetime import date
import database


class User:
    def __init__(self, isim,soyisim,sifre):
        self.isim = isim
        self.soyisim=soyisim
        self.sifre=sifre
        self.ek_gelir=0
        database.db_add_user(isim,soyisim,sifre)
        self.kullanici_id=database.get_user_id(isim,soyisim,sifre)

    def __str__(self):
        return f"Hoşgeldin {self.isim}!"

    def gider_kayit(self):
        aylik_gider_sayisi = int(input("kaç adet aylık gideriniz var?: "))
        for x in range(aylik_gider_sayisi):
            miktar = int(input(f"{x+1}. gider miktarı: "))
            kategori = "net_gider"
            gun = int(input(f"{x+1}. giderin gelme günü (1,15...): "))
            tarih = date.today().replace(day=gun)
            database.db_add_transaction(self.kullanici_id,kategori,miktar,gun,"gider",tarih)

    def gelir_kayit(self):
        aylik_gelir_sayisi = int(input("kaç adet aylık geliriniz var?: "))
        for x in range(aylik_gelir_sayisi):
            miktar = int(input(f"{x+1}. gelir miktarı: "))
            kategori = "net_gelir"
            gun = int(input(f"{x+1}. gelirin gelme günü (1,15...): "))
            tarih = date.today().replace(day=gun)
            database.db_add_transaction(self.kullanici_id,kategori,miktar,gun,"gelir",tarih)

    def gelir_gider_hesapla(self):
        self.net_gelir = sum(
            (
                t[3]
                for t in database.get_data(self.kullanici_id,"net_gelir","gelir")
            )
        )
        self.net_gider = sum(
            (
                t[3]
                for t in database.get_data(self.kullanici_id,"net_gider","gider")
            )
        )
        self.aylik_gider=0
        self.aylik_gider=sum(
            (
                t[3]
                for t in database.get_data(self.kullanici_id,"gunluk_gider","gider")
                if date.fromisoformat(t[6]) > date.today() - timedelta(days=30)
            )
        )
        self.net_kalan = self.net_gelir + self.ek_gelir - self.net_gider
        self.aylik_kalan = self.net_kalan-self.aylik_gider
        print(f"kalan para: {self.aylik_kalan}")
    def gunluk_gider(self):
        gunluk_gider_sayisi = int(input("bugün kaç adet harcama yaptınız:"))
        for x in range(gunluk_gider_sayisi):
            miktar = int(input(f"{x+1}. gider miktarı "))
            tarih = datetime.now().date()
            database.db_add_transaction(self.kullanici_id,"gunluk_gider",miktar,datetime.now().day,"gider",tarih)
        print(f"{gunluk_gider_sayisi} adet gider kaydedildi.")
        toplam = sum(t[3] for t in database.get_data(self.kullanici_id,"gunluk_gider","gider") if t[2] == "gunluk_gider" and date.fromisoformat(t[6]) == date.today())
        if toplam > (self.net_kalan/30):
            print("bugünkü gider olması gerekenden yüksek")
        else:
            print(f"bugün kalan gider limitiniz: {(self.net_kalan/30)-toplam}")
    def ek_gelir_ekle(self,miktar):
        self.ek_gelir+=miktar
        database.db_add_transaction(self.kullanici_id,"ek_gelir",miktar,datetime.now().day,"gelir",datetime.now().date())
        print(f"{miktar} TL ek gelir eklendi")