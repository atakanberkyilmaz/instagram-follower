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
echo [*] NOT: Bu script calisirken ilerleme durumunu gosterecektir.
echo [*] Sonuclar CMD ekraninda goruntulenecektir.
echo [*] Session otomatik kaydedilecek (bir sonraki calistirmada giris yapmaniza gerek yok).
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

echo.
echo [*] Sonuclari export etmek ister misiniz?
echo    1. Hayir (Sadece CMD'de goster)
echo    2. CSV dosyasi olarak kaydet
echo    3. JSON dosyasi olarak kaydet
echo    4. Her ikisini de kaydet (CSV + JSON)
set /p EXPORT_CHOICE="Seciminiz (1/2/3/4): "

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
echo [*] Lutfen bekleyin, islem biraz zaman alabilir...
echo [*] Ilerleme durumu ekranda goruntulenecektir.
echo [*] Session kaydedilecek, bir sonraki calistirmada giris yapmaniza gerek yok.
echo.

REM Export secimine gore parametre ekle
set EXPORT_PARAM=
if "%EXPORT_CHOICE%"=="2" set EXPORT_PARAM=--export csv
if "%EXPORT_CHOICE%"=="3" set EXPORT_PARAM=--export json
if "%EXPORT_CHOICE%"=="4" set EXPORT_PARAM=--export both

py main.py -u %USERNAME% -p %PASSWORD% -t %TARGET% %EXPORT_PARAM%
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
echo [*] Lutfen bekleyin, islem biraz zaman alabilir...
echo [*] Ilerleme durumu ekranda goruntulenecektir.
echo.

REM Export secimine gore parametre ekle
set EXPORT_PARAM=
if "%EXPORT_CHOICE%"=="2" set EXPORT_PARAM=--export csv
if "%EXPORT_CHOICE%"=="3" set EXPORT_PARAM=--export json
if "%EXPORT_CHOICE%"=="4" set EXPORT_PARAM=--export both

py main.py -t %TARGET% %EXPORT_PARAM%
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
echo [*] Sonuclar yukarida goruntulenmistir.
echo [*] Takip ettiginiz ancak sizi takip etmeyen hesaplar listelenmistir.

REM Export yapildiysa bilgi ver
if "%EXPORT_CHOICE%"=="2" (
    echo [*] Sonuclar CSV dosyasina kaydedildi.
)
if "%EXPORT_CHOICE%"=="3" (
    echo [*] Sonuclar JSON dosyasina kaydedildi.
)
if "%EXPORT_CHOICE%"=="4" (
    echo [*] Sonuclar hem CSV hem de JSON dosyalarina kaydedildi.
)

pause

