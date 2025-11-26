# Instagram Follower Analiz Aracı

---

## ⚠️ PROJE ASKIYA ALINDI ⚠️

> **Durum:** 🚫 **AKTİF DEĞİL**  
> **Tarih:** Kasım 2025  
> **Sebep:** Instagram hesap ban'ı  

### Ne Oldu?
Instagram tarafından hesaba ban uygulandığı için bu script şu an kullanılamaz durumda. API erişimi engellendiğinden dolayı proje geçici olarak rafa kaldırıldı.

### Ban Çözülene Kadar:
- ❌ Yeni commit atılmayacak
- ❌ Script test edilemeyecek
- ❌ Aktif geliştirme yapılmayacak
- ⏳ Proje bekleme modunda

### Çözüm Önerileri (araştırılacak):
- [ ] Instagram hesap itirazı yapılması
- [ ] Farklı bir hesap ile test edilmesi
- [ ] Proxy kullanımı değerlendirilmesi
- [ ] API rate limiting stratejisinin gözden geçirilmesi

---

## 📋 Proje Hakkında

Bu Python scripti, belirli bir Instagram hesabında takip analizi yapmanıza olanak sağlar.

## Özellikler

- ✅ Belirli bir hesabın takipçilerini listeler
- ✅ Belirli bir hesabın takip ettiği hesapları listeler
- ✅ Takip edilen ancak takip etmeyen hesapları bulur (one-way followers)
- ✅ Sonuçları dosyaya kaydeder

## Kurulum

1. Python 3.7 veya üzeri sürümün yüklü olduğundan emin olun
2. Gerekli paketleri yükleyin:

```bash
# Windows için:
py -m pip install -r requirements.txt

# veya
python -m pip install -r requirements.txt

# Linux/Mac için:
pip install -r requirements.txt
```

## Kullanım

### Temel Kullanım

```bash
# Windows için:
py main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI

# veya
python main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI

# Linux/Mac için:
python main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI
```

### Parametreler

- `-u, --username`: Instagram kullanıcı adınız (giriş için gerekli)
- `-p, --password`: Instagram şifreniz
- `-t, --target`: Analiz edilecek hedef Instagram kullanıcı adı
- `--non-followers-only`: Sadece takip etmeyenleri göster
- `--following-only`: Sadece takip edilenleri göster

### Örnekler

```bash
# Tüm analizi yap (takip edilenler ve takip etmeyenler)
py main.py -u benim_kullanici_adi -p benim_sifrem -t hedef_kullanici

# Sadece takip etmeyenleri bul
py main.py -u benim_kullanici_adi -p benim_sifrem -t hedef_kullanici --non-followers-only

# Sadece takip edilenleri listele
py main.py -u benim_kullanici_adi -p benim_sifrem -t hedef_kullanici --following-only
```

## Çıktılar

Script çalıştırıldığında şu dosyalar oluşturulur:

- `{hedef_kullanici}_non_followers.txt`: Takip edilen ancak takip etmeyen hesaplar
- `{hedef_kullanici}_following.txt`: Takip edilen tüm hesaplar

## Önemli Notlar

⚠️ **Uyarılar:**

- Instagram API limitleri nedeniyle büyük hesaplarda işlem uzun sürebilir
- Rate limiting nedeniyle script otomatik olarak bekleme süreleri ekler
- İki faktörlü doğrulama (2FA) aktifse, kod girişi istenecektir
- Instagram'ın kullanım şartlarına uygun kullanın

## Gereksinimler

- Python 3.7+
- instagrapi kütüphanesi

## Lisans

Bu proje açık kaynaklıdır.
