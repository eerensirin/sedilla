from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget,QListWidgetItem,
    QComboBox, QHBoxLayout, QGridLayout, QMessageBox, QStackedWidget,
    QFrame)
from PyQt5.QtGui import QFont,QPixmap
from PyQt5.QtCore import Qt,QSize
import sys
from functools import partial
from urun_takip import UrunTakip
import os
class SiparisYonetim(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SİPARİŞ TAKİP")
        self.setGeometry(100, 100, 1000, 650)
        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #242424, stop:1 #3a3a3a);
    }
""")
        def resource_path(relative_path):
            """ Kaynak dosyalarının yolunu ayarlar (exe veya script çalıştırırken). """
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        

        
        self.urun_takip = UrunTakip()  # Ürün takibini başlat
        self.layout = QHBoxLayout()
        self.toplam_fiyat = 0
        self.sira_numarasi = 1
        self.kategori_layout = QVBoxLayout()
        self.kategoriler = [
            "Çorbalar", "Salatalar", "Soslu Tavuklar", "Makarnalar",
            "Ekstralar", "Tatlılar", "Yan Lezzetler", "İçecekler"
        ]
        self.kategori_renkleri = {
        "Çorbalar": "#FF5733",  # Kırmızımsı turuncu
        "Salatalar": "#4CAF50",  # Yeşil
        "Soslu Tavuklar": "#FF9800",  # Turuncu
        "Makarnalar": "#F4A261",  # Açık turuncu
        "Ekstralar": "#9C27B0",  # Mor
        "Tatlılar": "#E91E63",  # Pembe
        "Yan Lezzetler": "#795548",  # Kahverengi
        "İçecekler": "#2196F3"   # Mavi
    }
        for kategori in self.kategoriler:
            renk = self.kategori_renkleri.get(kategori, "#007AFF")  # Varsayılan olarak mavi
            kategori_buton = QPushButton(kategori)
            kategori_buton.setStyleSheet(f"""
                QPushButton {{
                    padding: 12px;
                    font-size: 16px;
                    border-radius: 8px;
                    background-color: {renk};
                    color: white;
                    border: 2px solid {renk};
                }}
                QPushButton:hover {{
                    background-color: {renk[:-2]}AA;  /* Hover efekti için şeffaf renk */
                }}
                QPushButton:pressed {{
                    background-color: {renk[:-2]}88;
                    border: 2px solid {renk[:-2]}66;
                }}
            """)
            kategori_buton.clicked.connect(partial(self.kategori_degistir_buton, kategori))
            self.kategori_layout.addWidget(kategori_buton)

        self.layout.addLayout(self.kategori_layout, 1)  # Kategori butonlarını ekle
        self.stacked_widget = QStackedWidget()
        self.urun_sayfalar = {}
        self.urunler = {
            "Çorbalar": {"Mercimek": 75, "Tavuk Suyu": 75,},
            "Salatalar": {"Sedilla Salata": 179, "Sezar Salata": 169},
            "Soslu Tavuklar": {"Acılı Barbekü": 209, "Köri Soslu Tavuk": 209},
            "Makarnalar": {"Sedilla Fettucine": 159, "Fettucine Alfredo": 159, "Pesto Soslu Fettucine": 159, "Tavuk Mantar Penne": 139, "Köri Penne": 139, "Sedilla Special Penne": 159},
            "Ekstralar": {"Ekstra Tavuk": 40, "Ekstra Parmesan": 40, "Ekstra Havuç Tarator": 40, "Ekstra Köz Patlıcan": 40, "Ekstra Mantar": 40, "Ekstra Krema": 40, "Ekstra Mozzarella": 40},
            "Tatlılar": {"Waffle": 189, "Sufle": 169, "Fondü Tabağı": 169, "Kazandibi": 109, "Fırın Sütlaç": 109, "Dondurma Top": 30},
            "Yan Lezzetler": {"Ev Mantısı": 139},
            "İçecekler": {"Meşrubat": 50, "Sade Soda": 25, "Meyveli Soda": 35, "Ayran": 40, "Su": 10, "Çay": 25, "Filtre Kahve": 70, "Türk Kahvesi": 50}
        }

        
        
        for kategori, urunler in self.urunler.items():
            sayfa = QWidget()
            grid = QGridLayout()
            row, col = 0, 0
            buton_genislik, buton_yukseklik, resim_genislik, resim_yukseklik = self.boyutlandir(len(urunler))
            
            # Dinamik boyutlandırma fonksiyonu:
            if urunler:
                if len(urunler) <= 6:
                    buton_genislik, buton_yukseklik = 300, 250
                    resim_genislik, resim_yukseklik = 280, 180
                elif len(urunler) <= 10:
                    buton_genislik, buton_yukseklik = 250, 220
                    resim_genislik, resim_yukseklik = 230, 150
                else:
                    buton_genislik, buton_yukseklik = 200, 160
                    resim_genislik, resim_yukseklik = 180, 120

            grid = QGridLayout()
            row, col = 0, 0

            for urun, fiyat in urunler.items():
                buton = QPushButton()
                buton.setFixedSize(buton_genislik, buton_yukseklik)

                # Görsel için QLabel oluştur
                resim_yolu = resource_path(f"icons/{urun.lower().replace(' ', '_')}.jpg")
                resim_label = QLabel()
                resim_label.setAlignment(Qt.AlignCenter)

                if os.path.exists(resim_yolu):
                    pixmap = QPixmap(resim_yolu)
                    resim_label.setPixmap(pixmap.scaled(resim_genislik, resim_yukseklik, Qt.KeepAspectRatio))
                else:
                    resim_label.setText("Görsel Yok")
                    resim_label.setStyleSheet("color: white; font-size: 14px;")

                text_label = QLabel(f"{urun.upper()}\n{fiyat} TL")
                text_label.setAlignment(Qt.AlignCenter)
                text_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        background-color: rgba(0,0,0,0.5);
                        border-radius: 5px;
                        padding: 4px;
                    }
                """)

                # Layout oluştur (buton içeriği)
                layout = QVBoxLayout()
                layout.addWidget(resim_label, 3)
                layout.addWidget(text_label, 1)

                # Butonu oluştur ve layoutu ekle
                buton = QPushButton()
                buton.setLayout(layout)
                buton.setFixedSize(buton_genislik, buton_yukseklik)
                buton.setCheckable(False)
                buton.setStyleSheet("""
                    QPushButton {
                        border: 2px solid #007AFF;
                        border-radius: 12px;
                        background-color: transparent;
                    }
                    QPushButton:hover {
                        border-color: #0056b3;
                    }
                    QPushButton:pressed {
                        border-color: #004494;
                    }
                """)

                buton.clicked.connect(partial(self.urun_secildi, buton=buton, urun=urun, fiyat=fiyat))

                # Porsiyon seçim kutusu
                porsiyon_secimi = QComboBox()
                porsiyon_secimi.addItems(["1 Porsiyon", "1.5 Porsiyon", "2 Porsiyon"])
                porsiyon_secimi.setStyleSheet("""
                QComboBox {
                    background-color: #333;
                    color: white;
                    font-size: 18px;
                    padding: 8px;
                    border-radius: 8px;
                    border: 2px solid #007AFF;
                    min-width: 150px;
                }
                QComboBox QAbstractItemView {
                    background-color: #555;
                    color: white;
                    selection-background-color: #007AFF;
                    selection-color: white;
                    font-size: 18px;
                }
                QComboBox:hover {
                    border-color: #3399FF;
                }
                QComboBox::drop-down {
                    width: 30px;
                }
            """)
                porsiyon_secimi.setFixedWidth(buton_genislik)
                porsiyon_secimi.currentIndexChanged.connect(partial(self.porsiyon_degisti, buton, urun, fiyat))

                buton.porsiyon_secimi = porsiyon_secimi

                # Grid’e ekleme
                grid.addWidget(buton, row, col)
                grid.addWidget(porsiyon_secimi, row, col + 1, alignment=Qt.AlignLeft | Qt.AlignVCenter)
                col += 2
                if col > 2:
                    col = 0
                    row += 1

            sayfa.setLayout(grid)
            self.urun_sayfalar[kategori] = sayfa
            self.stacked_widget.addWidget(sayfa)

        self.layout.addWidget(self.stacked_widget, 3)
        self.siparis_layout = QVBoxLayout()
        self.siparis_label = QLabel("Sipariş Özeti")
        self.siparis_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.siparis_label.setStyleSheet("padding: 10px;")
        self.siparis_listesi = QListWidget()
        self.siparis_listesi.setStyleSheet("""
            QListWidget {
                background: #222;
                border-radius: 10px;
                padding: 5px;
                color: white;
                font-size: 16px;
                border: 2px solid #444;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #555;
            }
            QListWidget::item:selected {
                background: #007AFF;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        self.siparis_listesi.itemClicked.connect(self.siparis_sil)
        self.toplam_label = QLabel("Toplam: 0 TL")
        self.toplam_label.setFont(QFont("Arial", 12))
        self.toplam_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #32D74B;
                padding: 10px;
            }
        """)
        self.siparis_layout.addWidget(self.siparis_label)
        self.siparis_layout.addWidget(self.siparis_listesi)
        self.siparis_layout.addWidget(self.toplam_label)
        self.siparis_tamamla_buton = QPushButton("Siparişi Excele Aktar")
        self.siparis_tamamla_buton.setStyleSheet("""
    QPushButton {
        padding: 14px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 12px;
        background-color: #32D74B;
        color: white;
        border: 2px solid #28B33D;
    }
    QPushButton:hover {
        background-color: #28B33D;
    }
    QPushButton:pressed {
        background-color: #1F8F2A;
        border: 2px solid #166B20;
    }
""")
        self.siparis_tamamla_buton.clicked.connect(self.siparis_tamamla)
        self.siparis_layout.addWidget(self.siparis_tamamla_buton)
        self.layout.addLayout(self.siparis_layout, 2)
        self.setLayout(self.layout)

    def porsiyon_degisti(self, buton, urun, fiyat):
        porsiyon_secimi = buton.porsiyon_secimi  # Butona bağlı QComboBox'ı kullan
        porsiyon = porsiyon_secimi.currentText()
        yeni_fiyat = fiyat * 1.5 if "1.5 Porsiyon" in porsiyon else fiyat * 2 if "2 Porsiyon" in porsiyon else fiyat
        buton.setText(f"{urun}\n{yeni_fiyat} TL")
        buton.setProperty("guncel_fiyat", yeni_fiyat)  # Güncellenmiş fiyatı butona ata

    def kategori_degistir_buton(self, kategori_adi):
        kategori_index = self.kategoriler.index(kategori_adi)  # Kategori listesindeki index'i bul
        self.stacked_widget.setCurrentIndex(kategori_index)  # Sayfayı değiştir

    def urun_secildi(self, buton, urun, fiyat):
        # Güncellenmiş fiyatı al
        guncel_fiyat = buton.property("guncel_fiyat") or fiyat  # Eğer property yoksa fiyatı kullan
        item = QListWidgetItem(f"{urun} - {guncel_fiyat} TL")
        item.setData(Qt.UserRole, guncel_fiyat)  # Fiyatı veri olarak ekle
        self.siparis_listesi.addItem(item)
        # Toplam fiyatı güncelle
        self.toplam_fiyat += guncel_fiyat
        self.toplam_label.setText(f"Toplam: {self.toplam_fiyat} TL")
        # Siparişi UrunTakip'e ekle
        self.urun_takip.siparis_ekle(urun, guncel_fiyat)

    def boyutlandir(self, urun_sayisi):
        if urun_sayisi <= 4:
            return (300, 250, 280, 180)  # (buton genişlik, buton yükseklik, resim genişlik, resim yükseklik)
        elif urun_sayisi <= 8:
            return (250, 200, 230, 150)
        elif urun_sayisi <= 12:
            return (200, 160, 180, 120)
        else:
            return (150, 130, 140, 90)


    def siparis_sil(self, item):
        fiyat = item.data(Qt.UserRole)  # Direkt veriyi al
        if fiyat is not None:
            self.toplam_fiyat -= fiyat
            self.toplam_label.setText(f"Toplam: {self.toplam_fiyat} TL")
            urun_adi = item.text().split(" - ")[0]  # Ürün adını al
            self.siparis_listesi.takeItem(self.siparis_listesi.row(item))

            # Siparişi UrunTakip'ten sil
            self.urun_takip.siparis_sil(urun_adi)

    def siparis_tamamla(self):
        if self.siparis_listesi.count() == 0:
            QMessageBox.warning(self, "Hata", "Sipariş listeniz boş!")
            return
        QMessageBox.information(self, "Sipariş Onayı", f"Sipariş Tamamlandı!\nToplam: {self.toplam_fiyat} TL")
        # Sipariş listesini hızlıca temizle
        self.siparis_listesi.clear()
        self.toplam_fiyat = 0
        self.toplam_label.setText("Toplam: 0 TL")

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = SiparisYonetim()
    pencere.show()
    sys.exit(app.exec_())
