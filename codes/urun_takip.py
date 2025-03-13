import pandas as pd
import os
from datetime import datetime

class UrunTakip:
    def __init__(self):
        self.siparisler = []  # Siparişleri listede tut

    def siparis_ekle(self, urun, fiyat):
        """Sipariş ekleyip Excel'e kaydeder"""
        saat = datetime.now().strftime("%H:%M:%S")  # Saat bilgisini al
        self.siparisler.append({"Saat": saat, "Ürün": urun, "Fiyat": fiyat})
        self.siparisleri_excele_yaz()

    def siparis_sil(self, urun):
        """Siparişi listeden siler ve Excel'e kaydeder"""
        self.siparisler = [s for s in self.siparisler if s["Ürün"] != urun]
        self.siparisleri_excele_yaz()

    def siparisleri_excele_yaz(self):
        """Mevcut siparişleri Excel dosyasına kaydeder ve analiz oluşturur"""
        tarih = datetime.now().strftime("%d-%m-%y")
        dosya_adi = f"Sedilla-{tarih}-Satis_Listesi.xlsx"

        # Sipariş Listesi Sayfası için DataFrame
        if self.siparisler:
            df_siparisler = pd.DataFrame(self.siparisler)
        else:
            df_siparisler = pd.DataFrame(columns=["Saat", "Ürün", "Fiyat"])  # Boş liste

        # **GENEL ANALİZ HESAPLAMALARI**
        if not df_siparisler.empty:
            # Ürün Bazlı Satış Analizi
            urun_satis_sayisi = df_siparisler["Ürün"].value_counts().reset_index()
            urun_satis_sayisi.columns = ["Ürün", "Satış Adedi"]

            # Saat Bazlı Satış Analizi
            saat_satis_sayisi = df_siparisler["Saat"].value_counts().reset_index()
            saat_satis_sayisi.columns = ["Saat", "Satış Sayısı"]
            saat_satis_sayisi = saat_satis_sayisi.sort_values("Saat")  # Saat sırasına göre sırala

            # Günlük Toplam Kazanç
            toplam_kazanc = df_siparisler["Fiyat"].sum()

            # En Çok Satılan Ürün
            en_cok_satis = urun_satis_sayisi.iloc[0] if not urun_satis_sayisi.empty else ["-", 0]

            # En Az Satılan Ürün
            en_az_satis = urun_satis_sayisi.iloc[-1] if not urun_satis_sayisi.empty else ["-", 0]

            # Analizleri DataFrame olarak oluştur
            df_genel_analiz = pd.DataFrame({
                "Özellik": ["Toplam Kazanç", "En Çok Satılan Ürün", "En Az Satılan Ürün"],
                "Değer": [toplam_kazanc, f"{en_cok_satis['Ürün']} ({en_cok_satis['Satış Adedi']} adet)", 
                          f"{en_az_satis['Ürün']} ({en_az_satis['Satış Adedi']} adet)"]
            })
        else:
            df_genel_analiz = pd.DataFrame(columns=["Özellik", "Değer"])
            urun_satis_sayisi = pd.DataFrame(columns=["Ürün", "Satış Adedi"])
            saat_satis_sayisi = pd.DataFrame(columns=["Saat", "Satış Sayısı"])

        # Excel'e kaydetme işlemi
        with pd.ExcelWriter(dosya_adi, engine="xlsxwriter") as writer:
            df_siparisler.to_excel(writer, sheet_name="Sipariş Listesi", index=False)
            df_genel_analiz.to_excel(writer, sheet_name="Genel Analiz", index=False)
            urun_satis_sayisi.to_excel(writer, sheet_name="Genel Analiz", startrow=5, index=False)
            saat_satis_sayisi.to_excel(writer, sheet_name="Genel Analiz", startrow=10+len(urun_satis_sayisi), index=False)
