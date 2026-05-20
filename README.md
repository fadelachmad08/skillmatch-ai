# SkillMatch AI

**Discover Your Skills. Match Your Future.**

Career Readiness Recommender System untuk Mata Kuliah Foundations of Artificial Intelligence.

---

## FITUR

- **Analisis Skill** (Home) — Form input skill & dapat rekomendasi karier real-time
- **Edit Profile** — Simpan profil pribadi (nama, jurusan, skill) supaya tidak perlu input ulang
- **Riwayat Analisis** — Semua hasil analisis tersimpan otomatis, bisa di-review kapan saja
- **Chat AI** — Tanya AI tentang hasil analisis, skill gap, kursus, atau algoritma
- **Dataset Viewer** — Lihat 3 sheet dataset + heatmap visualisasi binary matrix
- **Algorithm Explainer** — Penjelasan lengkap cosine similarity dengan contoh perhitungan

---

## CARA MENJALANKAN

### Windows (Disarankan)

1. **Install Python** dari https://python.org/downloads (centang "Add Python to PATH")
2. **Double-click `run.bat`**
3. Browser otomatis terbuka ke http://localhost:5000

### Mac/Linux

```bash
chmod +x run.sh && ./run.sh
```

### Manual

```bash
pip install -r requirements.txt
python app.py
```

---

## JANGAN BUKA HTML LANGSUNG

Aplikasi ini butuh Flask server. **Jangan double-click `index.html`** — itu akan menyebabkan "Failed to fetch" dan dropdown kosong.

Selalu jalankan via `run.bat` atau `python app.py`, lalu buka http://localhost:5000.

---

## STRUKTUR PROYEK

```
skillmatch_ai/
├── run.bat                       # Launcher Windows (double-click)
├── run.sh                        # Launcher Mac/Linux
├── app.py                        # Flask web server (semua route)
├── recommender.py                # CORE AI (Cosine Similarity)
├── requirements.txt
├── README.md
├── data/
│   ├── SkillMatch_AI_Dataset.xlsx
│   └── storage/                  # (auto-generated)
│       ├── profile.json          # Profile user
│       └── history.json          # Riwayat analisis
├── static/
│   ├── logo.svg                  # Logo SkillMatch AI
│   └── style.css                 # Stylesheet (design system)
└── templates/
    ├── _header.html              # Shared header (nav bar)
    ├── index.html                # Home (analisis)
    ├── profile.html              # Edit profile
    ├── history.html              # Riwayat analisis
    ├── chat.html                 # Chat AI
    ├── dataset.html              # Dataset viewer
    └── algorithm.html            # Penjelasan algoritma
```

---

## BRAND IDENTITY

- **Primary colors:** Navy `#1D2B64`, Blue `#3B82F6`, Purple `#8B5CF6`
- **Font:** Poppins (SemiBold)
- **Tagline:** Discover Your Skills. Match Your Future.

---

## ALGORITMA AI

### Pipeline 4 Tahap:

1. **Vector Representation** — Setiap karier & user direpresentasikan sebagai binary vector 20-dimensi
2. **Cosine Similarity** — Hitung kemiripan vektor user vs karier
3. **Interest Boost** — Tambah +0.10 jika sesuai minat user
4. **Skill Gap Analysis + Course Mapping** — Identifikasi missing skills & mapping ke kursus

### Formula:

```
cos(θ) = (A · B) / (||A|| × ||B||)
final_score = min(cos_sim + interest_boost, 1.0)
```

### Contoh:

User: `[Python, SQL, Statistics, Excel, Tableau]` + minat `Data Analyst`
→ **94.5% match**, skill gap: `Data Visualization, Power BI`

---

## DATASET

File: `data/SkillMatch_AI_Dataset.xlsx`

| Sheet | Records | Format |
|---|---|---|
| Career_Skills | 10 karier | Binary vector (1/0) untuk 20 skill |
| Student_Profiles | 15 mahasiswa | Binary vector skill |
| Course_Recommendations | 19 kursus | Mapping skill → kursus (Coursera, Udemy, dll) |

---

## HALAMAN

| URL | Deskripsi |
|---|---|
| `/` | Home — analisis skill |
| `/profile` | Edit profile |
| `/history` | Riwayat analisis |
| `/chat` | Chat dengan AI |
| `/dataset` | Lihat dataset (3 sheet + heatmap) |
| `/algorithm` | Penjelasan algoritma lengkap |

---

## TROUBLESHOOTING

**"Failed to fetch" / dropdown kosong**
→ Jalankan via `run.bat`, bukan buka HTML langsung

**Port 5000 sudah dipakai**
→ Edit `app.py` baris terakhir, ganti port

**Module not found**
→ `pip install flask pandas scikit-learn numpy openpyxl`

---

**Created for Foundations of AI course**
