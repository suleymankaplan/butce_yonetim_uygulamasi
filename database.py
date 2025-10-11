import sqlite3
from datetime import datetime

DB_NAME="butce_yonetim.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    with connect_db() as conn:
        cursor=conn.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS islemler(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                kullanici_id INTEGER,
                                kategori TEXT,
                                miktar REAL NOT NULL,
                                gun INTEGER,
                                tur TEXT,
                                tarih DATE,
                                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id)
                            )
                        ''')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS kullanicilar(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            isim TEXT NOT NULL,
                            soyisim TEXT,
                            sifre TEXT
                        )
                        ''')
        conn.commit()
def show_table(table_name):
    with connect_db() as conn:
        cursor=conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(col) 
def db_add_user(isim,soyisim,sifre):
    with connect_db() as conn:
        cursor=conn.cursor()
        cursor.execute('''
                    INSERT INTO kullanicilar(isim,soyisim,sifre)
                    VALUES(?,?,?);
                    ''',(isim,soyisim,sifre))
        conn.commit()
def db_add_transaction(kullanici_id,kategori,miktar,gun,tur,tarih):
    with connect_db() as conn:
        cursor=conn.cursor()
        cursor.execute('''
                    INSERT INTO islemler(kullanici_id,kategori,miktar,gun,tur,tarih)
                    VALUES(?,?,?,?,?,?);
                    ''',(kullanici_id,kategori,miktar,gun,tur,tarih))
        conn.commit()
def get_user_id(isim,soyisim,sifre):
    with connect_db() as conn:
        cursor=conn.cursor()
        cursor.execute('''
                    SELECT id FROM kullanicilar WHERE isim=? AND soyisim=? AND sifre=?;
                    ''',(isim,soyisim,sifre))
        row=cursor.fetchone()
        return row[0] if row else None
def get_data(kullanici_id,kategori,tur):
    with connect_db() as conn:
        cursor=conn.cursor()
        if kategori or kategori==None:
            cursor.execute('''
                        SELECT * FROM islemler WHERE kullanici_id=? AND tur=? AND kategori=?
                        ''',(kullanici_id,tur,kategori))
        else:
            cursor.execute('''
                        SELECT * FROM islemler WHERE kullanici_id=? AND tur=?
                        ''',(kullanici_id,tur))
        data=cursor.fetchall()
        return data