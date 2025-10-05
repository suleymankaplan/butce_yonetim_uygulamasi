transactions=[]
class Transaction:
    def __init__(self,kategori,miktar,gun,tur,tarih):
        self.kategori=kategori
        self.miktar=miktar
        self.gun=gun
        self.tur=tur
        self.tarih=tarih
    def __str__(self):
        return f"[gün: {self.gun}] {self.kategori}: {self.miktar} TL ({self.tur})"
        