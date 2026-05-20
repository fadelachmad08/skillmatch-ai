"""
==========================================================================
SkillMatch AI - Recommendation Engine
==========================================================================
Module ini adalah JANTUNG dari sistem AI SkillMatch.

DATASET FORMAT: Binary Skill Vector
  - Setiap karier direpresentasikan sebagai vektor biner [1, 0, 1, 0, ...]
  - 1 = skill dibutuhkan / dimiliki, 0 = tidak
  - Format ini IDEAL untuk Cosine Similarity (skala uniform)

ALGORITMA:
1. Vector Space Model
   - Karier, mahasiswa, dan input user direpresentasikan dalam ruang vektor
     berdimensi N (N = jumlah skill di dataset)

2. Cosine Similarity
   - Mengukur kemiripan antara profil user dengan setiap karier
   - cos(theta) = (A . B) / (||A|| * ||B||)
   - Hasil: skor 0-1 (semakin tinggi = semakin cocok)

3. Skill Gap Analysis
   - Hitung selisih: skill yang dibutuhkan karier - skill yang dimiliki user
   - Output: daftar skill yang perlu dipelajari

4. Course Mapping
   - Pemetaan missing skills ke katalog kursus
   - Berdasarkan kolom "Skill" pada Course_Recommendations
==========================================================================
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os


class SkillMatchRecommender:
    def __init__(self, xlsx_path='data/SkillMatch_AI_Dataset.xlsx'):
        """Load dataset dari Excel dan siapkan vektor biner."""
        self.xlsx_path = xlsx_path

        # ----- Load 3 sheet -----
        # Header ada di row 3 (index 2), karena row 1-2 adalah title.
        self.careers_df = pd.read_excel(
            xlsx_path, sheet_name='Career_Skills', header=2
        )
        self.students_df = pd.read_excel(
            xlsx_path, sheet_name='Student_Profiles', header=2
        )
        self.courses_df = pd.read_excel(
            xlsx_path, sheet_name='Course_Recommendations', header=2
        )
        # Rename kolom courses biar jelas
        self.courses_df.columns = [
            'Skill', 'Nama Kursus', 'Platform', 'Level', 'Durasi', 'Link'
        ]

        # ----- Identifikasi kolom skill -----
        meta_cols = ['No', 'Karier', 'Kategori', 'Deskripsi', 'Total Skill']
        self.skill_columns = [
            c for c in self.careers_df.columns if c not in meta_cols
        ]

        # ----- Buat matriks vektor biner -----
        self.career_matrix = self.careers_df[self.skill_columns].values.astype(float)
        self.career_names = self.careers_df['Karier'].tolist()
        self.student_matrix = self.students_df[self.skill_columns].values.astype(float)

        print(f"[AI Model] Loaded {len(self.careers_df)} careers, "
              f"{len(self.students_df)} student profiles, "
              f"{len(self.courses_df)} course mappings")
        print(f"[AI Model] Skill vector dimension: {len(self.skill_columns)}")
        print(f"[AI Model] Career matrix shape: {self.career_matrix.shape}")

    def _build_user_vector(self, user_skills):
        """Ubah list skill user jadi vektor biner sesuai urutan skill_columns."""
        user_skills_lower = {s.strip().lower() for s in user_skills if s.strip()}
        vector = np.zeros(len(self.skill_columns))
        for i, col in enumerate(self.skill_columns):
            if col.lower() in user_skills_lower:
                vector[i] = 1.0
        return vector

    def recommend_career(self, user_skills, user_interest=None, top_n=3):
        """Rekomendasi karier berdasarkan vektor skill user."""
        user_vec = self._build_user_vector(user_skills).reshape(1, -1)

        # Handle edge case: user belum punya skill apapun
        if user_vec.sum() == 0:
            return []

        sims = cosine_similarity(user_vec, self.career_matrix)[0]

        results = []
        for i, sim in enumerate(sims):
            career = self.careers_df.iloc[i]
            boost = 0.10 if (user_interest and
                             user_interest.lower() in career['Karier'].lower()) else 0
            final = float(sim) + boost
            results.append({
                'career_name': career['Karier'],
                'category': career['Kategori'],
                'description': career['Deskripsi'],
                'total_skills_required': int(career['Total Skill']),
                'similarity_score': round(float(sim), 4),
                'final_score': round(min(final, 1.0), 4),
                'match_percentage': round(min(final * 100, 100), 1),
                'interest_match': boost > 0
            })

        results.sort(key=lambda x: x['final_score'], reverse=True)
        return results[:top_n]

    def analyze_skill_gap(self, user_skills, target_career_name):
        """Analisis skill gap: skill apa yang belum dimiliki user."""
        career_row = self.careers_df[
            self.careers_df['Karier'].str.lower() == target_career_name.lower()
        ]
        if career_row.empty:
            return None

        career = career_row.iloc[0]
        user_vec = self._build_user_vector(user_skills)

        career_vec = np.array(
            [career[col] for col in self.skill_columns]
        ).astype(float)

        required_skills = [
            self.skill_columns[i] for i in range(len(self.skill_columns))
            if career_vec[i] == 1
        ]
        matched_skills = [
            self.skill_columns[i] for i in range(len(self.skill_columns))
            if career_vec[i] == 1 and user_vec[i] == 1
        ]
        missing_skills = [
            self.skill_columns[i] for i in range(len(self.skill_columns))
            if career_vec[i] == 1 and user_vec[i] == 0
        ]
        readiness = (len(matched_skills) / len(required_skills) * 100
                     if required_skills else 0)

        return {
            'target_career': career['Karier'],
            'category': career['Kategori'],
            'description': career['Deskripsi'],
            'required_skills': required_skills,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'total_required': len(required_skills),
            'total_matched': len(matched_skills),
            'total_missing': len(missing_skills),
            'readiness_percentage': round(readiness, 1)
        }

    def recommend_courses(self, missing_skills):
        """Untuk setiap missing skill, cari kursus dari Course_Recommendations."""
        if not missing_skills:
            return []

        recommendations = []
        for skill in missing_skills:
            matched = self.courses_df[
                self.courses_df['Skill'].str.lower() == skill.lower()
            ]
            courses_for_skill = []
            for _, c in matched.iterrows():
                courses_for_skill.append({
                    'course_name': c['Nama Kursus'],
                    'platform': c['Platform'],
                    'level': c['Level'],
                    'duration': c['Durasi'],
                    'link': c['Link']
                })
            recommendations.append({
                'skill': skill,
                'courses': courses_for_skill,
                'course_count': len(courses_for_skill)
            })
        return recommendations

    def get_full_recommendation(self, user_data):
        """Pipeline lengkap: Input -> Career Rec -> Skill Gap -> Course Rec."""
        current_skills = user_data.get('current_skills', [])
        career_interest = user_data.get('career_interest', '')

        career_recs = self.recommend_career(
            current_skills,
            user_interest=career_interest,
            top_n=3
        )

        target_career = career_interest if career_interest else (
            career_recs[0]['career_name'] if career_recs else None
        )
        skill_gap = (self.analyze_skill_gap(current_skills, target_career)
                     if target_career else None)

        course_recs = []
        if skill_gap and skill_gap['missing_skills']:
            course_recs = self.recommend_courses(skill_gap['missing_skills'])

        return {
            'user': user_data,
            'recommended_careers': career_recs,
            'skill_gap_analysis': skill_gap,
            'course_recommendations': course_recs,
            'algorithm_info': {
                'method': 'Vector Space Model + Cosine Similarity',
                'skill_dimension': len(self.skill_columns),
                'total_careers': len(self.careers_df),
                'total_students_in_dataset': len(self.students_df),
                'total_courses': len(self.courses_df)
            }
        }

    def list_all_skills(self):
        """Untuk dropdown / checkbox di UI."""
        return self.skill_columns

    def list_all_careers(self):
        """Untuk dropdown minat karier di UI."""
        return self.careers_df[['Karier', 'Kategori']].to_dict('records')


# ============================================================
# DEMO / CLI mode
# ============================================================
if __name__ == '__main__':
    print("=" * 70)
    print(" SkillMatch AI - Demo Mode")
    print("=" * 70)

    DATA_PATH = os.path.join(
        os.path.dirname(__file__), 'data', 'SkillMatch_AI_Dataset.xlsx'
    )
    recommender = SkillMatchRecommender(xlsx_path=DATA_PATH)

    test_user = {
        'name': 'Fadel',
        'major': 'Sistem Informasi',
        'semester': 6,
        'career_interest': 'Data Analyst',
        'current_skills': ['Python', 'SQL', 'Statistics', 'Excel', 'Tableau']
    }

    print(f"\n[INPUT] User: {test_user['name']}")
    print(f"        Jurusan: {test_user['major']}, Semester {test_user['semester']}")
    print(f"        Minat: {test_user['career_interest']}")
    print(f"        Skill: {test_user['current_skills']}")

    result = recommender.get_full_recommendation(test_user)

    print("\n" + "=" * 70)
    print(" REKOMENDASI KARIER (Top 3)")
    print("=" * 70)
    for i, c in enumerate(result['recommended_careers'], 1):
        marker = ' (sesuai minat)' if c['interest_match'] else ''
        print(f"\n{i}. {c['career_name']} [{c['category']}] - "
              f"Match: {c['match_percentage']}%{marker}")
        print(f"   {c['description']}")
        print(f"   cosine_sim = {c['similarity_score']} | "
              f"final_score = {c['final_score']}")

    print("\n" + "=" * 70)
    print(" SKILL GAP ANALYSIS")
    print("=" * 70)
    gap = result['skill_gap_analysis']
    print(f"\nTarget: {gap['target_career']}")
    print(f"Readiness: {gap['readiness_percentage']}% "
          f"({gap['total_matched']}/{gap['total_required']} skill match)")
    print(f"\nSkill yang dibutuhkan ({gap['total_required']}): {gap['required_skills']}")
    print(f"Sudah dimiliki ({gap['total_matched']}): {gap['matched_skills']}")
    print(f"Perlu dipelajari ({gap['total_missing']}): {gap['missing_skills']}")

    print("\n" + "=" * 70)
    print(" REKOMENDASI KURSUS")
    print("=" * 70)
    for rec in result['course_recommendations']:
        print(f"\n-> Skill: {rec['skill']} ({rec['course_count']} kursus)")
        for c in rec['courses']:
            print(f"   * {c['course_name']} | {c['platform']} | "
                  f"{c['level']} | {c['duration']}")

    print("\n" + "=" * 70)
    info = result['algorithm_info']
    print(f" Algoritma   : {info['method']}")
    print(f" Skill dim   : {info['skill_dimension']}")
    print(f" Total karier: {info['total_careers']}")
    print(f" Total kursus: {info['total_courses']}")
    print("=" * 70)
