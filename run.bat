@echo off
chcp 65001 >nul
echo ========================================
echo Instagram Follower Analiz Araci
echo ========================================
echo.

REM Gerekli paketlerin yuklu oldugundan emin ol
echo [*] Gerekli paketler kontrol ediliyor...
py -m pip install -r requirements.txt >nul 2>&1

echo.
echo [*] Script baslatiliyor...
echo.

REM Hedef kullanici adini al
set /p TARGET="Analiz edilecek hedef kullanici adini girin: "

if "%TARGET%"=="" (
    echo [!] Hedef kullanici adi bos olamaz!
    pause
    exit /b 1
)

echo.
echo [*] Giris yapmak ister misiniz?
echo    1. Evet (Kesin sonuc icin giris yapin - tavsiye edilir)
echo    2. Hayir (Giris yapmadan deneyelim - Instagram genellikle engeller)
set /p LOGIN_CHOICE="Seciminiz (1/2): "

if "%LOGIN_CHOICE%"=="1" goto :login
if "%LOGIN_CHOICE%"=="2" goto :no_login
if /i "%LOGIN_CHOICE%"=="evet" goto :login
if /i "%LOGIN_CHOICE%"=="hayir" goto :no_login
if /i "%LOGIN_CHOICE%"=="hayir" goto :no_login

REM Varsayilan olarak giris yapmadan dene
echo.
echo [*] Gecersiz secim, giris yapmadan devam ediliyor...
goto :no_login

:login
echo.
set /p USERNAME="Instagram kullanici adinizi girin: "
set /p PASSWORD="Instagram sifrenizi girin: "

if "%USERNAME%"=="" (
    echo [!] Kullanici adi bos olamaz!
    pause
    exit /b 1
)

if "%PASSWORD%"=="" (
    echo [!] Sifre bos olamaz!
    pause
    exit /b 1
)

echo.
echo [*] Analiz baslatiliyor (giris yapilmis)...
echo.
py main.py -u %USERNAME% -p %PASSWORD% -t %TARGET%
if errorlevel 1 (
    echo.
    echo [!] Script calisirken bir hata olustu!
    pause
    exit /b 1
)
goto :end

:no_login
echo.
echo [*] Analiz baslatiliyor (giris yapilmadan)...
echo [*] Not: Instagram genellikle takipci ve takip edilen listelerini korumali tutar.
echo [*] Eger calismazsa, giris yaparak tekrar deneyin.
echo.
py main.py -t %TARGET%
if errorlevel 1 (
    echo.
    echo [!] Script calisirken bir hata olustu!
    pause
    exit /b 1
)
goto :end

:end
echo.
echo [*] Islem tamamlandi!
pause

