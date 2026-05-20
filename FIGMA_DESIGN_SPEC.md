# SkillMatch AI — Figma Design Spec

**Untuk dipakai sebagai panduan rebuild di Figma.**
File HTML preview ada di `figma_design_spec.html` — buka di browser untuk lihat visual setiap halaman.

---

## 🎨 Color Palette

### Primary Colors

| Name | Hex | Usage |
|---|---|---|
| Navy | `#1D2B64` | Heading text, primary text |
| Blue | `#3B82F6` | Primary action, link |
| Indigo | `#6366F1` | Gradient middle |
| Purple | `#8B5CF6` | Accent, gradient end |
| Lavender | `#EDE9FE` | Background highlight |

### Semantic Colors

| Name | Hex | Usage |
|---|---|---|
| Background | `#F8FAFF` | Page background |
| Paper | `#FFFFFF` | Card background |
| Muted | `#64748B` | Secondary text |
| Line | `#E2E8F0` | Borders, dividers |
| Success | `#10B981` | Success state |
| Danger | `#EF4444` | Error state |

### Primary Gradient
- **CSS:** `linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)`
- **Figma:** Linear gradient 135° dari #3B82F6 ke #8B5CF6
- **Usage:** Buttons, logo, score numbers, top match border

---

## ✍️ Typography — Poppins

Install di Figma: cari "Poppins" di font picker (Google Font, gratis).

| Style | Size | Weight | Line-height | Letter-spacing | Usage |
|---|---|---|---|---|---|
| Hero H1 | 48px | 700 | 1.1 | -1.5px | Main heading |
| Section H2 | 28px | 700 | 1.2 | -0.5px | Section title |
| Card title H3 | 22px | 700 | 1.3 | -0.3px | Card heading |
| Item H4 | 18px | 700 | 1.4 | 0 | Career name, course name |
| Body | 14px | 400/500 | 1.5 | 0 | Default text |
| Label | 13px | 600 | 1.4 | 0 | Form labels |
| Caption | 12px | 500 | 1.4 | 0 | Hint text |
| Eyebrow | 11px | 600 | 1 | 2px | Pre-heading tags |

---

## 📐 Spacing & Sizing

### Spacing Scale

| Token | Value | Usage |
|---|---|---|
| XS | 4px | Icon gap |
| SM | 8px | Tight gap |
| MD | 16px | Standard gap |
| LG | 24px | Card padding |
| XL | 32px | Section gap |
| 2XL | 48px | Major break |

### Border Radius

| Token | Value | Usage |
|---|---|---|
| SM | 8px | Chips internal |
| MD | 10px | Buttons, inputs |
| LG | 12px | Stat boxes |
| XL | 16px | Cards, sections |
| Full | 100px | Pills, chips |

### Frame Sizes

| Page | Dimensions |
|---|---|
| Desktop | 1440 × auto |
| Tablet | 768 × auto |
| Mobile | 375 × auto |

---

## 🧩 Components

### 1. Logo

- **Container:** 44×44px (header), 64×64px (large)
- **Border-radius:** 12px (header), 16px (large)
- **Background:** Primary gradient
- **Icon:** White star/spark in center
- **Text:** "SkillMatch" Navy + "AI" gradient text

### 2. Navigation Header

- **Height:** 76px
- **Padding:** 16px 0
- **Border-bottom:** 1px solid #E2E8F0
- **Nav links:**
  - Inactive: padding 8px 14px, font 14px/500, color Muted
  - Active: background gradient, color white, radius 8px
  - Hover: background Lavender, color Navy

### 3. Buttons

| Variant | Background | Text | Border |
|---|---|---|---|
| Primary | Gradient | White | none |
| Secondary | Lavender | Purple | none |
| Ghost | Transparent | Muted | 1.5px solid Line |
| Danger | Transparent | Danger | 1.5px solid #FECACA |

- **Size:** padding 12px 20px, radius 10px, font 14px/600
- **Small:** padding 6px 12px, font 12px

### 4. Input Field

- **Padding:** 11px 14px
- **Border:** 1.5px solid #E2E8F0
- **Radius:** 10px
- **Background:** White
- **Font:** 14px/500
- **Focus:** Border Blue + shadow `0 0 0 3px rgba(59, 130, 246, 0.12)`

### 5. Skill Checkbox

- **Container:** padding 7px 10px, radius 8px, font 12px/500
- **Default:** White background, 1px transparent border
- **Hover:** 1px solid Blue
- **Checked:** Gradient background, white text, checkmark icon
- **Grid:** 2 columns, gap 6px, max-height 280px scrollable

### 6. Chips

- **Padding:** 5px 12px
- **Radius:** 100px (full pill)
- **Font:** 12px/500
- **Variants:**
  - Skill: bg Lavender, text Purple
  - Have (matched): bg rgba(16,185,129,0.12), text #047857
  - Missing: bg rgba(239,68,68,0.12), text #B91C1C
  - Blue: bg rgba(59,130,246,0.12), text Blue

### 7. Cards

- **Background:** White
- **Border:** 1px solid #E2E8F0
- **Radius:** 16px
- **Padding:** 28px
- **Shadow:** `0 1px 2px rgba(29,43,100,0.05)`

### 8. Career Card

- **Layout:** 3 columns (rank | info | score)
- **Padding:** 18px
- **Border:** 1.5px solid Line
- **Radius:** 12px
- **TOP variant:**
  - 2px gradient border (use background-clip trick)
  - "TOP" badge top-right: gradient bg, white text, 10px font, 700 weight
  - Rank number with gradient fill

### 9. Match Score

- **Number:** 32px/700, gradient text fill
- **Label:** 10px/600 uppercase, color Muted

### 10. Stat Box

- **Background:** #F8FAFF
- **Border:** 1px solid Line
- **Radius:** 12px
- **Padding:** 16px
- **Number:** 32-36px/700, gradient fill
- **Label:** 10px/600 uppercase

### 11. Section Container

- **Background:** White
- **Border:** 1px solid Line
- **Radius:** 16px
- **Padding:** 28px
- **Header:** flex justify-between, border-bottom 1px Line, padding-bottom 12px
- **Step badge:** 11px/600 uppercase, bg Lavender, text Purple, radius 100px

### 12. Chat Bubble

- **Padding:** 12px 16px
- **Radius:** 16px (with 4px corner pointing to sender)
- **Font:** 14px/400, line-height 1.5
- **User:** Gradient bg, white text, right-aligned, radius 16/16/4/16
- **AI:** White bg, 1px Line border, left-aligned, radius 16/16/16/4
- **Time:** 10px/500, color Muted, margin-top 4px

### 13. Avatar (Profile)

- **Size:** 88×88px (profile page), 40×40px (chat)
- **Background:** Primary gradient
- **Border-radius:** 50% (circle)
- **Text:** First letter uppercase, white, 36px/700

### 14. AI Insight Box (Footer)

- **Background:** Primary gradient
- **Color:** White
- **Padding:** 20px 24px
- **Radius:** 12px
- **Font:** 13px/400, line-height 1.7
- **Label:** 10px/600 uppercase, color rgba(255,255,255,0.7)
- **Code tag:** bg rgba(255,255,255,0.18), radius 4px

---

## 📄 Page Layouts

### Page 1: HOME (1440 × 1600)

```
┌─────────────────────────────────────────────┐
│  [Header: Logo + Nav]                       │
├─────────────────────────────────────────────┤
│                                             │
│  [Hero Section]                             │
│  Tag · H1 (2 lines) · Description           │
│                                             │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐  ┌────────────────────┐    │
│  │             │  │ Section 1:         │    │
│  │  FORM CARD  │  │ Rekomendasi Karier │    │
│  │             │  │ ┌──┬─────────┬───┐ │    │
│  │ Nama        │  │ │1 │ Top     │ % │ │    │
│  │ Jurusan/Sem │  │ ├──┼─────────┼───┤ │    │
│  │ Minat       │  │ │2 │ Career  │ % │ │    │
│  │ Skill grid  │  │ ├──┼─────────┼───┤ │    │
│  │ [Button]    │  │ │3 │ Career  │ % │ │    │
│  │             │  │ └──┴─────────┴───┘ │    │
│  │             │  ├────────────────────┤    │
│  │             │  │ Section 2:         │    │
│  │             │  │ Skill Gap          │    │
│  │             │  │ [3 stat boxes]     │    │
│  │             │  │ [Have chips]       │    │
│  │             │  │ [Missing chips]    │    │
│  │             │  ├────────────────────┤    │
│  │             │  │ Section 3:         │    │
│  │             │  │ Kursus & Sertif    │    │
│  │             │  │ [Course blocks]    │    │
│  │             │  ├────────────────────┤    │
│  │             │  │ AI Insight Footer  │    │
│  └─────────────┘  └────────────────────┘    │
│   420px              flex-1                  │
└─────────────────────────────────────────────┘
```

### Page 2: PROFILE (1440 × 1200)

```
┌─────────────────────────────────────────────┐
│  [Header]                                   │
├─────────────────────────────────────────────┤
│  [Hero]                                     │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────┐  ┌──────────────────┐│
│  │ Avatar           │  │ Ringkasan        ││
│  │ Edit Form        │  │ - Nama: ...      ││
│  │                  │  │ - Jurusan: ...   ││
│  │ Name             │  │ - Sem: ...       ││
│  │ Major / Sem      │  │ - Minat: ...     ││
│  │ Career interest  │  │ - Total skill    ││
│  │ Skill grid       │  │ [skill chips]    ││
│  │                  │  ├──────────────────┤│
│  │ [Save] [Reset]   │  │ Quick Actions    ││
│  │                  │  │ → Analisis       ││
│  │                  │  │ → Riwayat        ││
│  │                  │  │ → Chat AI        ││
│  └──────────────────┘  └──────────────────┘│
└─────────────────────────────────────────────┘
```

### Page 3: HISTORY (1440 × 1000)

```
┌─────────────────────────────────────────────┐
│  [Header]                                   │
│  [Hero]                                     │
│  [2 stat cards]                             │
│  [Text + Clear All button]                  │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │ Title · Career     │ Score % │ 🗑   │    │
│  │ Date · Major · Sem │         │      │    │
│  ├─────────────────────────────────────┤    │
│  │ Title · Career     │ Score % │ 🗑   │    │
│  │ Date · Major · Sem │         │      │    │
│  ├─────────────────────────────────────┤    │
│  │ ...                                  │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### Page 4: CHAT AI (1440 × 1000)

```
┌─────────────────────────────────────────────┐
│  [Header]                                   │
│  [Hero]                                     │
│                                             │
│  ┌──────────────────────┐  ┌──────────┐    │
│  │ ChatHeader (avatar+status) │ Try   │    │
│  ├──────────────────────┤  │ asking: │    │
│  │ AI: Halo!            │  │ [chip]  │    │
│  │ User: Question →     │  │ [chip]  │    │
│  │ AI: Answer           │  │ [chip]  │    │
│  │ ...                  │  ├──────────┤    │
│  │                      │  │ Latest  │    │
│  │ (scrollable)         │  │ Analysis│    │
│  ├──────────────────────┤  └──────────┘    │
│  │ [Input] [Send btn]   │                  │
│  └──────────────────────┘                  │
└─────────────────────────────────────────────┘
```

---

## 🚀 Cara Pakai di Figma

### Setup Awal (sekali saja)

1. **Buat file Figma baru** atau buka file `WIREFRAME` kamu
2. **Setup color styles:**
   - Klik kanvas → Right panel → Local styles → klik `+` di "Colors"
   - Tambahkan 10 warna di atas satu per satu (Navy, Blue, Indigo, Purple, Lavender, dst)
3. **Setup text styles:**
   - Right panel → Local styles → klik `+` di "Text"
   - Pilih font **Poppins**, tambahkan 8 style di atas (Hero H1, Section H2, dst)
4. **Setup effect (shadow):**
   - Drop shadow card: X=0, Y=1, Blur=2, Color=#1D2B6420 (5% navy)

### Recreate Halaman

**Opsi A — Pakai HTML Preview:**
1. Buka file `figma_design_spec.html` di browser
2. Screenshot setiap frame (gunakan Fullpage screenshot tool)
3. Drag screenshot ke Figma sebagai reference layer (opacity 50%)
4. Recreate elemen di atasnya pakai shapes & text Figma

**Opsi B — Build From Scratch:**
1. Buat frame 1440×auto untuk setiap page
2. Ikuti layout di atas
3. Pakai style yang sudah disetup

### Tips Cepat

- **Component-ize semua reusable elements** dulu (Button, Input, Card, Chip, etc) supaya bisa di-update sekali, kena semua
- **Pakai Auto-layout** di setiap card/section supaya responsive
- **Mulai dari Home page**, karena paling rich. Halaman lain reuse component dari Home.
- **Logo:** Bisa screenshot dari brand guide yang sudah kamu kirim, atau pakai SVG yang sudah saya bikin di `static/logo.svg`

---

## 📋 Checklist Build di Figma

### Foundation
- [ ] Color styles (10 warna)
- [ ] Text styles (8 style Poppins)
- [ ] Shadow effect style
- [ ] Logo component (44px & 64px variants)

### Components
- [ ] Button (4 variants: Primary, Secondary, Ghost, Danger)
- [ ] Input field
- [ ] Skill checkbox (default & checked state)
- [ ] Chip (4 variants)
- [ ] Card container
- [ ] Career card (default & top variant)
- [ ] Stat box
- [ ] Section container
- [ ] Navigation header
- [ ] Chat bubble (user & AI)
- [ ] Avatar (large 88px & small 40px)

### Pages
- [ ] Home (form + 3 result sections)
- [ ] Profile (form + summary)
- [ ] History (list view)
- [ ] Chat AI (conversation + sidebar)
- [ ] Dataset (optional, time permitting)
- [ ] Algorithm (optional, time permitting)

### Prototyping
- [ ] Nav links: connect ke setiap page
- [ ] Button "Analisis Profil": connect ke result state
- [ ] Suggestion chips di chat: connect ke message reply

---

**Total estimasi waktu Figma:** 4-8 jam (tergantung familiarity dengan Figma)
