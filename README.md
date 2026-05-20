---
title: SkillMatch AI
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: AI-powered Career Readiness Recommender
---

# SkillMatch AI

**Discover Your Skills. Match Your Future.**

Career Readiness Recommender System untuk Mata Kuliah Foundations of Artificial Intelligence.

## FITUR

- **Analisis Skill** (Home) — Form input skill & dapat rekomendasi karier real-time
- **Edit Profile** — Simpan profil pribadi (nama, jurusan, skill)
- **Riwayat Analisis** — Semua hasil analisis tersimpan otomatis
- **Chat AI** — Tanya AI tentang hasil analisis, skill gap, kursus, atau algoritma
- **Dataset Viewer** — Lihat 3 sheet dataset + heatmap visualisasi binary matrix
- **Algorithm Explainer** — Penjelasan lengkap cosine similarity dengan contoh perhitungan

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

## DATASET

File: `data/SkillMatch_AI_Dataset.xlsx`

| Sheet | Records | Format |
|---|---|---|
| Career_Skills | 10 karier | Binary vector (1/0) untuk 20 skill |
| Student_Profiles | 15 mahasiswa | Binary vector skill |
| Course_Recommendations | 19 kursus | Mapping skill → kursus |

## HALAMAN

| URL | Deskripsi |
|---|---|
| `/` | Home — analisis skill |
| `/profile` | Edit profile |
| `/history` | Riwayat analisis |
| `/chat` | Chat dengan AI |
| `/dataset` | Lihat dataset (3 sheet + heatmap) |
| `/algorithm` | Penjelasan algoritma lengkap |

## TECH STACK

- Backend: Flask + Gunicorn
- AI: scikit-learn (Cosine Similarity), pandas, numpy
- Frontend: HTML, CSS, JavaScript (vanilla)
- Deployment: Docker on Hugging Face Spaces

## LOCAL DEVELOPMENT

```bash
pip install -r requirements.txt
python app.py
```

Buka http://localhost:5000

---

**Created for Foundations of AI course**
