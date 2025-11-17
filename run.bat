@echo off
chcp 65001 >nul
echo ========================================
echo Instagram Follower Analiz Aracı
echo ========================================
echo.

REM Gerekli paketlerin yüklü olduğundan emin ol
echo [*] Gerekli paketler kontrol ediliyor...
py -m pip install -r requirements.txt >nul 2>&1

echo.
echo [*] Script baslatiliyor...
echo.

REM Hedef kullanıcı adını al
set /p TARGET="Analiz edilecek hedef kullanici adini girin: "

echo.
echo [*] Giriş yapmak ister misiniz?
echo    1. Evet (Kesin sonuc icin giris yapin - tavsiye edilir)
echo    2. Hayir (Giris yapmadan deneyelim - Instagram genellikle engeller)
set /p LOGIN_CHOICE="Seciminiz (1/2): "

if "%LOGIN_CHOICE%"=="1" (
    echo.
    set /p USERNAME="Instagram kullanici adinizi girin: "
    set /p PASSWORD="Instagram sifrenizi girin: "
    echo.
    echo [*] Analiz baslatiliyor (giris yapilmis)...
    echo.
    py main.py -u %USERNAME% -p %PASSWORD% -t %TARGET%
) else (
    echo.
    echo [*] Analiz baslatiliyor (giris yapilmadan)...
    echo [*] Not: Instagram genellikle takipci ve takip edilen listelerini korumali tutar.
    echo [*] Eger calismazsa, giris yaparak tekrar deneyin.
    echo.
    py main.py -t %TARGET%
)

echo.
echo [*] Islem tamamlandi!
pause

