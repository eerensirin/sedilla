# sedilla
Bir makarna dükkanı için ürün ve sipariş takip uygulaması Uygulamada PyQt, xlsxwriter ve pandas kütüphaneleri kullanılmıştır

pip install pyqt xlsxwriter pandas

komutuyla gerekli kütüphaneleri terminalden yükleyebilirsiniz.

pyinstaller --noconsole --onefile --name SedillaApp --add-data "icons;icons" siparis_takip.py

komutu ile uygulamanızı diğer bilgisayarlarda da çalışabilen bir exe dosyasına dönüştürebilirsiniz. Uygulamaya dönüştürürken lütfen terminalin dosya yolunu, sedilla klasörü içinde seçin

pycache dosyasının ve sonradan oluşturulan build dosyalarınının bir önemi yok silebilrisiniz.

urun_takip.py den excel in oluşturulma biçimini ve oluşturma ayarlarını düzenleyebilir ve geliştirebilirsiniz.
