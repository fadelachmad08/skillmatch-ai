#!/bin/bash
# ====================================================================
# SkillMatch AI - Mac/Linux Launcher
# ====================================================================

cd "$(dirname "$0")"

echo ""
echo "===================================================================="
echo " SkillMatch AI - Setup & Launcher"
echo "===================================================================="
echo ""

# Cek Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 tidak ditemukan!"
    echo "Install Python dari: https://python.org/downloads"
    exit 1
fi

echo "[OK] Python terdeteksi"
python3 --version

echo ""
echo "[INFO] Memastikan dependencies terinstall..."
python3 -m pip install -q -r requirements.txt 2>/dev/null || \
    python3 -m pip install -q --user -r requirements.txt 2>/dev/null || \
    python3 -m pip install -q --break-system-packages -r requirements.txt

echo ""
echo "===================================================================="
echo " Server akan terbuka di: http://localhost:5000"
echo " Tekan CTRL+C untuk menghentikan server."
echo "===================================================================="
echo ""

# Buka browser otomatis (Mac & Linux)
(sleep 3 && (open http://localhost:5000 2>/dev/null || xdg-open http://localhost:5000 2>/dev/null)) &

python3 app.py
