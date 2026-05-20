@echo off
REM ====================================================================
REM SkillMatch AI - Windows Launcher
REM Double-click file ini untuk menjalankan aplikasi
REM ====================================================================

cd /d "%~dp0"
title SkillMatch AI - Server

echo.
echo ====================================================================
echo  SkillMatch AI - Setup ^& Launcher
echo ====================================================================
echo.

REM Cek Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan!
    echo Install Python dari: https://python.org/downloads
    echo Pastikan centang "Add Python to PATH" saat install.
    echo.
    pause
    exit /b 1
)

echo [OK] Python terdeteksi
python --version

REM Install dependencies (silent kalau sudah ada)
echo.
echo [INFO] Memastikan dependencies terinstall...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [WARN] Gagal install otomatis, mencoba dengan --user...
    python -m pip install -q --user -r requirements.txt
)

echo.
echo ====================================================================
echo  Server akan terbuka di: http://localhost:5000
echo  Browser akan terbuka otomatis dalam 3 detik.
echo  Tekan CTRL+C di jendela ini untuk menghentikan server.
echo ====================================================================
echo.

REM Buka browser otomatis setelah 3 detik
start "" /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

REM Jalankan Flask
python app.py

pause
