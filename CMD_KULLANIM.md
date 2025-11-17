# CMD Kullanım Kılavuzu

## Hızlı Başlangıç

### 1. Gerekli Paketleri Yükle

```cmd
pip install -r requirements.txt
```

### 2. Scripti Çalıştır

#### Temel Kullanım:
```cmd
python main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI
```

#### Örnek:
```cmd
python main.py -u benim_kullanici_adi -p benim_sifrem -t hedef_kullanici
```

## Alternatif Yöntemler

### Batch Dosyası ile Çalıştırma (Kolay Yöntem)

```cmd
run.bat
```

Bu dosya sizi adım adım yönlendirecek ve gerekli bilgileri soracaktır.

### Sadece Takip Etmeyenleri Bul

```cmd
python main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI --non-followers-only
```

### Sadece Takip Edilenleri Listele

```cmd
python main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI --following-only
```

## Parametreler

| Parametre | Açıklama | Zorunlu |
|-----------|----------|---------|
| `-u, --username` | Instagram kullanıcı adınız | Evet |
| `-p, --password` | Instagram şifreniz | Evet |
| `-t, --target` | Analiz edilecek hedef kullanıcı | Evet |
| `--non-followers-only` | Sadece takip etmeyenleri göster | Hayır |
| `--following-only` | Sadece takip edilenleri göster | Hayır |

## Örnek Senaryolar

### Senaryo 1: Kendi Hesabınızı Analiz Etme

```cmd
python main.py -u benim_kullanici_adi -p benim_sifrem -t benim_kullanici_adi
```

### Senaryo 2: Başka Bir Hesabı Analiz Etme

```cmd
python main.py -u benim_kullanici_adi -p benim_sifrem -t baska_bir_kullanici
```

### Senaryo 3: Sadece Takip Etmeyenleri Bulma

```cmd
python main.py -u benim_kullanici_adi -p benim_sifrem -t hedef_kullanici --non-followers-only
```

## Çıktı Dosyaları

Script çalıştıktan sonra şu dosyalar oluşturulur:

- `{hedef_kullanici}_non_followers.txt` - Takip edilen ancak takip etmeyen hesaplar
- `{hedef_kullanici}_following.txt` - Takip edilen tüm hesaplar

## Sorun Giderme

### Python Bulunamadı Hatası

Eğer `python` komutu çalışmıyorsa, şunları deneyin:

```cmd
python3 main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI
```

veya

```cmd
py main.py -u KULLANICI_ADI -p SIFRE -t HEDEF_KULLANICI
```

### Paket Yükleme Hatası

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

### İki Faktörlü Doğrulama (2FA)

Eğer hesabınızda 2FA aktifse, script size kod girişi için izin verecektir.

## Notlar

⚠️ **Önemli:**
- Şifrenizi komut satırında görünür şekilde yazmak güvenli değildir
- Büyük hesaplarda işlem uzun sürebilir
- Instagram rate limit'leri nedeniyle script otomatik bekleme süreleri ekler

