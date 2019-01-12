"""
Bir projemde lazım olduğu için geliştirdiğim bir bot, internette benzer veriler olsa da güncelliğini yitirmiş olabiliyor.
Mesela yeni büyükşehir olan bir ilin ilçelerinin değişmesi gibi, bot direkt olarak Nüfus ve Vatandaşlık İşleri Genel
Müdürlüğü'nün güncel verilerini aldığı için güncelliğinden emin olunabilir.

    # Yazar: Halil ÖNCEN

    # 12 Ocak 2019 bir cumartesi öğleden sonrası (:
"""
import requests


class İlİlçeBotu:

    # Sınıfın kurucusu ilk ayarlamalar..
    def __init__(self):
        self._oturum = requests.session()  # Oturum kullanarak tüm istekleri tek TCP bağlantısı üzerinden daha hızlı gönderiyorum.
        # NVI api isteklerinde bir sorun çıkarsa headers içindeki cookie değerlerini değiştirmeniz gerekebilir.
        self._ayarlar = {
            'headers': {
            'Cookie': "__RequestVerificationToken=X9yWaztu8CZbFSmpCjGL0Q5K_Ndou1ub98l86D5QyTDm5Haek__O4ZM0qUPK_aMJ32bERlIo1txUVjAKSsW8VjxN8Zs1",
            'X-Requested-With': "XMLHttpRequest",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Referer': "https://adres.nvi.gov.tr/VatandasIslemleri/AdresSorgu",
            '__RequestVerificationToken': "ifs0dT-PkD9m41cTqWSZAv0oAu6ar2H1pRqqpZJ7IiO0lCbUC8wCQ9XH_03PtrfZVtFl7Vak_NloY7gMkDcgm8rhiFY1",
            'cache-control': "no-cache",
        },
            'iller_adresi': 'https://adres.nvi.gov.tr/Harita/ilListesi',
            'ilçeler_adresi': 'https://adres.nvi.gov.tr/Harita/ilceListesi'
        }

    # Tüm illeri {'09': 'AYDIN'} formatında plaka kodu ve ismiyle geri döndürür.
    def _illeri_getir(self):
        sonuç = {}
        iller = self._oturum.request('POST', self._ayarlar['iller_adresi'], headers=self._ayarlar['headers']).json()
        for il in iller:
            sonuç[il['kimlikNo']] = il['adi']
        return sonuç

    # Gönderilen plaka koduna göre söz konusu ilin tüm ilçelerini ['EFELER', 'SÖKE', ...] formatında geri döndürür.
    def _ilçeleri_getir(self, plaka):
        sonuç = []
        d = 'ilKimlikNo=' + str(plaka)
        ilçeler = self._oturum.request('POST', self._ayarlar['ilçeler_adresi'], data=d, headers=self._ayarlar['headers']).json()
        for ilçe in ilçeler:
            sonuç.append(ilçe['adi'])
        return sonuç

    # Çalıştırıldığı dizinde sonuçları, iller_ilçeler.json dosyasına kaydeder.
    def _iller_ilçeler_kaydet(self, iller_ilçeler):
        print('Kaydediliyor..')
        with open('iller_ilçeler.json', 'w') as dosya:
            print(iller_ilçeler, file=dosya)
            print('#Kaydedildi.')

    # Daha fazla modülerlik, daha esnek ve yönetilebilir kod ;)
    def _iller_ilçeler_getir(self):
        print('Tüm iller alınıyor..')
        iller_ilçeler = {}
        ilçe_sayısı = 0
        iller = self._illeri_getir()
        print(' -> {} il alındı!'.format(len(iller)))
        for il in iller:
            print('   #{} ilçeleri alınıyor..'.format(iller[il]))
            ilçeler = self._ilçeleri_getir(il)
            ilçe_sayısı += len(ilçeler)
            iller_ilçeler[iller[il]] = ilçeler
            print('      +{} ilçe alındı!'.format(len(ilçeler)))
        print('Tüm iller ve ilçeler alındı! --- {} il, {} ilçe'.format(len(iller), ilçe_sayısı))
        self._iller_ilçeler_kaydet(iller_ilçeler)

    # Botu başlatır.
    def başlat(self):
        self._iller_ilçeler_getir()


# Komut satırından başlatmak için
if __name__ == '__main__':
    İlİlçeBotu().başlat()
