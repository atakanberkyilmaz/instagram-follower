@echo off
chcp 65001 >nul
echo ========================================
echo Instagram Follower Analiz Aracı
echo ========================================
echo.

REM Gerekli paketlerin yüklü olduğundan emin ol
echo [*] Gerekli paketler kontrol ediliyor...
py -m pip install -r requirements.txt

echo.
echo [*] Script başlatılıyor...
echo.

REM Kullanıcı bilgilerini al
set /p USERNAME="Instagram kullanıcı adınızı girin: "
set /p PASSWORD="Instagram şifrenizi girin: "
set /p TARGET="Analiz edilecek hedef kullanıcı adını girin: "

echo.
echo [*] Analiz başlatılıyor...
echo.

REM Scripti çalıştır
py main.py -u %USERNAME% -p %PASSWORD% -t %TARGET%

echo.
echo [*] İşlem tamamlandı!
pause

