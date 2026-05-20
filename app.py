"""
==========================================================================
SkillMatch AI - Flask Web Application (v2)
==========================================================================
Fitur baru di versi ini:
- Edit Profile (CRUD profile user, disimpan di profile.json)
- Riwayat Analisis (history, disimpan di history.json)
- Chat dengan AI (Q&A tentang hasil rekomendasi, rule-based)
==========================================================================
"""

from flask import Flask, render_template, request, jsonify, session
from recommender import SkillMatchRecommender
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'skillmatch-ai-secret-key-2026'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'SkillMatch_AI_Dataset.xlsx')
STORAGE_DIR = os.path.join(BASE_DIR, 'data', 'storage')
os.makedirs(STORAGE_DIR, exist_ok=True)

PROFILE_FILE = os.path.join(STORAGE_DIR, 'profile.json')
HISTORY_FILE = os.path.join(STORAGE_DIR, 'history.json')

recommender = SkillMatchRecommender(xlsx_path=DATA_PATH)


# ============================================================
# STORAGE HELPERS (JSON-based persistence)
# ============================================================
def load_json(path, default):
    """Safely load JSON file with fallback default."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json(path, data):
    """Atomically save JSON data."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_profile():
    return load_json(PROFILE_FILE, {
        'name': '',
        'major': '',
        'semester': 1,
        'career_interest': '',
        'saved_skills': []
    })


def get_history():
    return load_json(HISTORY_FILE, [])


# ============================================================
# ROUTES - PAGES
# ============================================================
@app.route('/')
def index():
    """Halaman utama - form input user dengan auto-fill dari profile."""
    profile = get_profile()
    return render_template(
        'index.html',
        careers=recommender.list_all_careers(),
        skills=recommender.list_all_skills(),
        profile=profile,
        history_count=len(get_history())
    )


@app.route('/profile')
def profile_page():
    """Halaman edit profile."""
    return render_template(
        'profile.html',
        profile=get_profile(),
        skills=recommender.list_all_skills(),
        careers=recommender.list_all_careers(),
        history_count=len(get_history())
    )


@app.route('/history')
def history_page():
    """Halaman riwayat analisis."""
    history = get_history()
    # Urutkan dari terbaru
    history = sorted(history, key=lambda x: x.get('timestamp', ''), reverse=True)
    return render_template(
        'history.html',
        history=history,
        history_count=len(history)
    )


@app.route('/chat')
def chat_page():
    """Halaman chat dengan AI."""
    return render_template(
        'chat.html',
        history_count=len(get_history()),
        latest_result=(get_history()[-1] if get_history() else None)
    )


@app.route('/dataset')
def dataset_view():
    """Halaman untuk melihat dataset."""
    careers_list = []
    for _, row in recommender.careers_df.iterrows():
        skills = [s for s in recommender.skill_columns if row[s] == 1]
        careers_list.append({
            'no': int(row['No']),
            'name': row['Karier'],
            'category': row['Kategori'],
            'description': row['Deskripsi'],
            'skills': skills,
            'total_skills': int(row['Total Skill'])
        })

    students_list = []
    for _, row in recommender.students_df.iterrows():
        skills = [s for s in recommender.skill_columns if row[s] == 1]
        students_list.append({
            'id': row['Student ID'],
            'name': row['Nama'],
            'jurusan': row['Jurusan'],
            'semester': int(row['Semester']),
            'target': row['Target Karier'],
            'skills': skills,
            'total_skills': int(row['Total Skill']),
            'readiness': float(row['% Kesiapan']) * 100
        })

    courses_list = recommender.courses_df.to_dict('records')

    return render_template(
        'dataset.html',
        careers=careers_list,
        students=students_list,
        courses=courses_list,
        skill_columns=recommender.skill_columns,
        careers_count=len(careers_list),
        students_count=len(students_list),
        courses_count=len(courses_list),
        history_count=len(get_history())
    )


@app.route('/algorithm')
def algorithm_view():
    """Halaman penjelasan algoritma."""
    return render_template(
        'algorithm.html',
        skill_dim=len(recommender.skill_columns),
        career_count=len(recommender.careers_df),
        course_count=len(recommender.courses_df),
        history_count=len(get_history())
    )


# ============================================================
# API ENDPOINTS
# ============================================================
@app.route('/recommend', methods=['POST'])
def recommend():
    """API untuk mendapatkan rekomendasi + simpan ke history."""
    data = request.get_json()

    raw_skills = data.get('current_skills', [])
    if isinstance(raw_skills, str):
        current_skills = [s.strip() for s in raw_skills.split(',') if s.strip()]
    else:
        current_skills = [s.strip() for s in raw_skills if s and s.strip()]

    user_data = {
        'name': data.get('name', 'User'),
        'major': data.get('major', ''),
        'semester': data.get('semester', 1),
        'career_interest': data.get('career_interest', ''),
        'current_skills': current_skills
    }

    try:
        result = recommender.get_full_recommendation(user_data)

        # Simpan ke history
        history_entry = {
            'id': str(uuid.uuid4())[:8],
            'timestamp': datetime.now().isoformat(),
            'timestamp_display': datetime.now().strftime('%d %b %Y, %H:%M'),
            'user': user_data,
            'result': result
        }
        history = get_history()
        history.append(history_entry)
        # Batasi 50 history terakhir
        if len(history) > 50:
            history = history[-50:]
        save_json(HISTORY_FILE, history)

        result['history_id'] = history_entry['id']
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/profile/save', methods=['POST'])
def save_profile():
    """Simpan profile."""
    data = request.get_json()
    profile = {
        'name': data.get('name', ''),
        'major': data.get('major', ''),
        'semester': int(data.get('semester', 1)),
        'career_interest': data.get('career_interest', ''),
        'saved_skills': data.get('saved_skills', [])
    }
    save_json(PROFILE_FILE, profile)
    return jsonify({'status': 'success', 'profile': profile})


@app.route('/profile/reset', methods=['POST'])
def reset_profile():
    """Reset profile ke kosong."""
    if os.path.exists(PROFILE_FILE):
        os.remove(PROFILE_FILE)
    return jsonify({'status': 'success'})


@app.route('/history/<history_id>')
def history_detail(history_id):
    """Detail satu entry history (JSON)."""
    history = get_history()
    entry = next((h for h in history if h['id'] == history_id), None)
    if not entry:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(entry)


@app.route('/history/delete/<history_id>', methods=['DELETE'])
def history_delete(history_id):
    """Hapus satu entry history."""
    history = get_history()
    history = [h for h in history if h['id'] != history_id]
    save_json(HISTORY_FILE, history)
    return jsonify({'status': 'success'})


@app.route('/history/clear', methods=['POST'])
def history_clear():
    """Hapus semua history."""
    save_json(HISTORY_FILE, [])
    return jsonify({'status': 'success'})


# ============================================================
# AI CHAT - Rule-based Q&A about results
# ============================================================
@app.route('/chat/ask', methods=['POST'])
def chat_ask():
    """Chat AI: jawab pertanyaan user tentang rekomendasi & algoritma.

    Pendekatan: Rule-based / keyword matching dengan akses ke:
    - History terbaru (jika ada)
    - Dataset karier & skill
    - Pengetahuan tentang algoritma
    """
    data = request.get_json()
    question = data.get('question', '').lower().strip()

    if not question:
        return jsonify({'answer': 'Silakan ketik pertanyaan kamu dulu.'})

    history = get_history()
    latest = history[-1] if history else None
    answer = _generate_chat_answer(question, latest)
    return jsonify({'answer': answer})


def _generate_chat_answer(q, latest_result):
    """Rule-based answer generator."""
    has_result = latest_result is not None

    # ===== Pertanyaan tentang hasil rekomendasi =====
    if any(kw in q for kw in ['karier terbaik', 'karir terbaik', 'rekomendasi terbaik',
                              'paling cocok', 'karier saya', 'karir saya']):
        if not has_result:
            return ("Kamu belum melakukan analisis. Silakan ke halaman <b>Home</b> "
                    "dan klik 'Analisis Profil' dulu ya.")
        top = latest_result['result']['recommended_careers'][0]
        return (f"Berdasarkan analisis terakhir, karier yang paling cocok untuk kamu "
                f"adalah <b>{top['career_name']}</b> dengan match <b>{top['match_percentage']}%</b>. "
                f"{top['description']}")

    if any(kw in q for kw in ['skill gap', 'skill kurang', 'belum punya', 'perlu belajar',
                              'perlu dipelajari', 'kekurangan', 'skill apa', 'apa yang harus',
                              'apa yg harus', 'apa yang perlu', 'apa yg perlu',
                              'kurang apa', 'belum bisa', 'harus belajar']):
        if not has_result:
            return "Lakukan analisis dulu di halaman Home ya, baru saya bisa lihat skill gap kamu."
        gap = latest_result['result']['skill_gap_analysis']
        if not gap or not gap['missing_skills']:
            return ("Selamat! Kamu sudah punya semua skill yang dibutuhkan untuk karier target. "
                    "Tinggal asah lebih dalam saja.")
        missing = ', '.join(gap['missing_skills'])
        return (f"Untuk jadi <b>{gap['target_career']}</b>, kamu perlu belajar "
                f"<b>{gap['total_missing']} skill lagi</b>: {missing}. "
                f"Kesiapanmu saat ini {gap['readiness_percentage']}%.")

    if any(kw in q for kw in ['kursus', 'belajar dari mana', 'rekomendasi kursus', 'course']):
        if not has_result:
            return "Lakukan analisis dulu ya, baru saya bisa rekomendasikan kursus."
        courses = latest_result['result']['course_recommendations']
        if not courses:
            return "Belum ada kursus yang direkomendasikan karena skill kamu sudah lengkap!"
        text = "Berikut kursus yang saya rekomendasikan:<br><br>"
        for rec in courses[:3]:
            if rec['courses']:
                c = rec['courses'][0]
                text += (f"• <b>{rec['skill']}</b>: {c['course_name']} ({c['platform']}, "
                        f"{c['level']}, {c['duration']})<br>")
        return text

    if any(kw in q for kw in ['match', 'persentase', 'berapa persen', 'kecocokan',
                              'skor', 'kesiapan']):
        if not has_result:
            return "Lakukan analisis dulu ya. Saya akan jelaskan persentase kecocokan kamu."
        top = latest_result['result']['recommended_careers'][0]
        gap = latest_result['result']['skill_gap_analysis']
        return (f"Match kamu untuk karier <b>{top['career_name']}</b> adalah "
                f"<b>{top['match_percentage']}%</b>. Tingkat kesiapan: "
                f"<b>{gap['readiness_percentage']}%</b> ({gap['total_matched']} dari "
                f"{gap['total_required']} skill sudah dimiliki).")

    # ===== Pertanyaan tentang algoritma =====
    if any(kw in q for kw in ['algoritma', 'cara kerja', 'bagaimana', 'how it works',
                              'cosine', 'similarity']):
        return ("SkillMatch AI menggunakan <b>Vector Space Model + Cosine Similarity</b>. "
                "Setiap karier direpresentasikan sebagai vektor biner 20-dimensi (1 = skill "
                "dibutuhkan, 0 = tidak). Saat kamu input skill, sistem juga membuat vektor user, "
                "lalu menghitung cosine similarity dengan setiap karier. "
                "Cek detail lengkap di halaman <b>Algoritma</b>.")

    if any(kw in q for kw in ['tf-idf', 'tfidf']):
        return ("Sistem ini menggunakan <b>binary vector</b> langsung, bukan TF-IDF. "
                "Alasannya: dataset kami sudah dalam format binary (1/0) yang ideal untuk "
                "Cosine Similarity. TF-IDF lebih cocok untuk teks bebas dengan frekuensi kata.")

    if any(kw in q for kw in ['dataset', 'data nya', 'data set', 'sumber data']):
        return ("Dataset kami terdiri dari 3 sheet: <b>Career_Skills</b> (10 karier dengan "
                "binary vector skill), <b>Student_Profiles</b> (15 profil mahasiswa training), "
                "dan <b>Course_Recommendations</b> (19 kursus dari Coursera, Udemy, dll). "
                "Lihat lengkap di halaman <b>Dataset</b>.")

    # ===== Pertanyaan tentang karier tertentu =====
    for _, career in recommender.careers_df.iterrows():
        if career['Karier'].lower() in q:
            required = [s for s in recommender.skill_columns if career[s] == 1]
            return (f"<b>{career['Karier']}</b> ({career['Kategori']})<br>"
                    f"{career['Deskripsi']}<br><br>"
                    f"Membutuhkan <b>{int(career['Total Skill'])} skill</b>: "
                    f"{', '.join(required)}")

    # ===== Pertanyaan umum =====
    if any(kw in q for kw in ['hai', 'halo', 'hello', 'hi ']):
        return ("Halo! Saya AI Assistant SkillMatch. Saya bisa bantu jelaskan tentang "
                "hasil rekomendasi kamu, skill gap, kursus yang disarankan, atau "
                "cara kerja algoritma. Tanya apa saja ya!")

    if any(kw in q for kw in ['terima kasih', 'thanks', 'thx', 'makasih']):
        return "Sama-sama! Semangat mengejar karier impianmu ya!"

    if any(kw in q for kw in ['bantu', 'help', 'bisa apa', 'fitur']):
        return ("Saya bisa bantu kamu dengan:<br>"
                "• Penjelasan hasil rekomendasi kamu<br>"
                "• Detail skill gap dan kursus yang disarankan<br>"
                "• Info tentang setiap karier di dataset<br>"
                "• Cara kerja algoritma AI (Cosine Similarity)<br>"
                "• Pertanyaan umum tentang SkillMatch AI<br><br>"
                "Coba tanya: <i>'Apa karier terbaik untuk saya?'</i> atau "
                "<i>'Bagaimana cara kerja AI ini?'</i>")

    # Default fallback
    return ("Maaf, saya belum memahami pertanyaan itu. Coba tanya tentang:<br>"
            "• Hasil rekomendasi kamu<br>"
            "• Skill gap atau kursus<br>"
            "• Karier tertentu (Data Analyst, UI/UX Designer, dll)<br>"
            "• Algoritma yang digunakan<br><br>"
            "Atau ketik 'bantu' untuk daftar fitur.")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_production = os.environ.get('RENDER') is not None

    if not is_production:
        print("\n" + "=" * 70)
        print(" SkillMatch AI - Server Starting")
        print(" Buka browser dan akses:")
        print(f"   http://localhost:{port}           (Home - Analisis Skill)")
        print(f"   http://localhost:{port}/profile   (Edit Profile)")
        print(f"   http://localhost:{port}/history   (Riwayat Analisis)")
        print(f"   http://localhost:{port}/chat      (Chat dengan AI)")
        print(f"   http://localhost:{port}/dataset   (Lihat Dataset)")
        print(f"   http://localhost:{port}/algorithm (Penjelasan Algoritma)")
        print(" Tekan CTRL+C untuk berhenti.")
        print("=" * 70 + "\n")

    app.run(debug=False, host='0.0.0.0', port=port)
