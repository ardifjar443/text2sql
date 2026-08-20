# Text-to-SQL DTSEN

Sistem **Natural Language to SQL (Text-to-SQL)** yang mentransformasikan pertanyaan berbahasa Indonesia menjadi query SQL menggunakan **Large Language Model (LLM)** dengan pendekatan **embedding-based schema retrieval**.

Penelitian ini berfokus pada evaluasi model **LLaMA** dalam menghasilkan query SQL pada basis data **Data Tunggal Sosial Ekonomi Nasional (DTSEN)** serta menganalisis pengaruh schema retrieval berbasis embedding terhadap kualitas dan efisiensi generasi SQL.

---

## 📌 Deskripsi

Sistem ini menggunakan pipeline Text-to-SQL yang terdiri dari:

```text
Natural Language Question
        │
        ▼
Question Embedding
        │
        ▼
Schema Retrieval
        │
        ▼
Relevant Schema
        │
        ▼
Prompt Construction
        │
        ▼
LLaMA / LLM
        │
        ▼
Generated SQL
        │
        ▼
SQL Execution
        │
        ▼
Evaluation
```

Pendekatan schema retrieval digunakan untuk memberikan model hanya informasi schema yang relevan terhadap pertanyaan, sehingga konteks yang diberikan kepada model menjadi lebih ringkas dibandingkan penggunaan seluruh schema.

---

## 🎯 Tujuan Penelitian

Penelitian ini memiliki beberapa tujuan utama:

1. Menganalisis kemampuan model LLaMA dalam mentransformasikan pertanyaan bahasa alami menjadi query SQL pada basis data DTSEN.
2. Menganalisis efektivitas teknik embedding dalam proses schema retrieval sebelum generasi query SQL.
3. Membandingkan performa konfigurasi **full schema** dan **schema retrieval berbasis embedding** berdasarkan Exact Match dan Execution Accuracy.
4. Menganalisis pengaruh schema retrieval terhadap efisiensi konteks prompt dan kualitas query SQL yang dihasilkan.

---

## 🗄️ Dataset

### DTSEN

Dataset utama yang digunakan adalah **Data Tunggal Sosial Ekonomi Nasional (DTSEN)** dengan cakupan:

* Wilayah: **Kecamatan Pangatikan**
* Tahun data: **2025**
* DBMS: **MySQL**
* Jumlah pertanyaan pengujian: **53**
* Bahasa pertanyaan: **Bahasa Indonesia**

Dataset DTSEN digunakan sebagai dataset utama untuk seluruh eksperimen LLaMA.

### Dataset Eksternal

Untuk menguji kemampuan generalisasi arsitektur, sistem juga diuji pada dataset Text-to-SQL eksternal:

* **Resep**
* **Sakila**

Dataset eksternal digunakan untuk mengevaluasi apakah arsitektur schema retrieval yang digunakan dapat diterapkan pada database dengan struktur dan domain yang berbeda.

---

## 🧠 Model

Model yang digunakan dalam eksperimen meliputi:

### Model Utama

* LLaMA 3.2 1B Instruct
* LLaMA 3.2 3B Instruct
* LLaMA 3.1 8B Instruct
* LLaMA 3.3 70B Instruct

### Model Pembanding

* LLaMA 4 Maverick
* Gemini 3.7 Flash
* Gemini 2.5 Flash
* Gemini 3.5 Flash Lite
* GPT-5.6 Terra

Model pembanding digunakan untuk melihat performa pendekatan yang dikembangkan dibandingkan model generatif lainnya.

---

## 🔎 Schema Retrieval

Schema retrieval dilakukan menggunakan embedding untuk menentukan tabel dan kolom yang relevan terhadap pertanyaan.

Tahapan retrieval:

1. Informasi schema direpresentasikan menjadi teks.
2. Representasi schema diubah menjadi embedding.
3. Pertanyaan pengguna diubah menjadi embedding.
4. Embedding pertanyaan dibandingkan dengan embedding schema menggunakan **Cosine Similarity**.
5. Schema diurutkan berdasarkan tingkat relevansi.
6. Schema yang relevan dimasukkan ke dalam prompt model.

### Embedding Model

Model embedding yang digunakan:

**Google Gemini Embedding-2**

Representasi schema mencakup informasi seperti:

* Nama tabel
* Deskripsi tabel
* Primary key
* Foreign key
* Nama kolom
* Tipe data
* Deskripsi kolom

---

## ⚙️ Retrieval Method

Beberapa konfigurasi retrieval diuji dalam penelitian:

* Full Schema
* Top-K Retrieval
* Adaptive Mean
* Adaptive Gap
* Adaptive Percentile

Berdasarkan hasil pengujian pada DTSEN, **adaptive_mean** dipilih sebagai konfigurasi retrieval utama karena menghasilkan Execution Accuracy tertinggi pada pengujian schema retrieval.

---

## 📝 Prompt

Prompt digunakan sebagai konteks bagi LLM untuk menghasilkan query SQL berdasarkan pertanyaan dan schema yang diperoleh dari proses retrieval.

Komponen utama prompt meliputi:

* Role dan tujuan model
* SQL rules
* Table selection rules
* Alias rules
* Privacy rules
* Aggregation rules
* Business rules
* Semantic mapping
* Database schema
* User question
* Output instruction

Prompt lengkap yang digunakan dalam penelitian dapat ditemukan pada dokumentasi/lampiran penelitian.

---

## 📊 Evaluation

Sistem dievaluasi menggunakan beberapa metrik.

### Exact Match (EM)

Mengukur apakah query SQL yang dihasilkan identik dengan Ground Truth.

```text
EM = jumlah query identik / jumlah seluruh query × 100%
```

### Execution Accuracy (EX)

Mengukur apakah query hasil generasi dapat menghasilkan keluaran yang sesuai dengan Ground Truth ketika dijalankan pada database.

### Efficiency

Selain akurasi, sistem mencatat:

* Prompt Tokens
* Completion Tokens
* Total Tokens
* Latency

Parameter tersebut digunakan untuk menganalisis efisiensi penggunaan konteks dan waktu generasi.

---

## 📈 Hasil Utama

Pada pengujian DTSEN dengan konfigurasi `adaptive_mean`, performa Execution Accuracy menunjukkan peningkatan seiring ukuran model:

| Model         | Execution Accuracy |
| ------------- | -----------------: |
| LLaMA 3.2 1B  |              3.77% |
| LLaMA 3.2 3B  |             26.42% |
| LLaMA 3.1 8B  |             54.72% |
| LLaMA 3.3 70B |         **94.34%** |

Pada LLaMA 3.3 70B, perbandingan konfigurasi menunjukkan:

| Konfigurasi   | Exact Match | Execution Accuracy |
| ------------- | ----------: | -----------------: |
| Full Schema   |      45.28% |             84.91% |
| Adaptive Mean |  **47.17%** |         **94.34%** |

Hasil tersebut menunjukkan bahwa schema retrieval dapat meningkatkan Execution Accuracy sekaligus mengurangi jumlah konteks yang diberikan kepada model.

---

## 🏗️ Struktur Project

```text
text-to-sql/
│
├── config/
│   └── ...
│
├── services/
│   ├── embedding_service.py
│   ├── evaluation_service.py
│   ├── llm_service.py
│   ├── mini_schema_service.py
│   ├── prompt_service.py
│   └── schema_service.py
│
├── prompts/
│   └── ...
│
├── schemas/
│   └── ...
│
├── datasets/
│   └── ...
│
├── testing/
│   └── ...
│
├── config.py
├── requirements.txt
└── README.md
```

> Struktur folder dapat berbeda sesuai versi project yang digunakan.

---

## 🔄 Pipeline Pengujian

Contoh proses pengujian:

```text
Question
   │
   ▼
Load Prompt Template
   │
   ▼
Load Database Schema
   │
   ▼
Generate Question Embedding
   │
   ▼
Retrieve Relevant Tables
   │
   ▼
Retrieve Relevant Columns
   │
   ▼
Build Mini Schema
   │
   ▼
Build Prompt
   │
   ▼
Generate SQL
   │
   ▼
Execute SQL
   │
   ├── Exact Match
   ├── Execution Accuracy
   ├── Token Usage
   └── Latency
```

---

## 🛠️ Teknologi

Teknologi utama yang digunakan:

* Python
* MySQL
* Laragon
* LLaMA
* Gemini Embedding-2
* Cosine Similarity
* REST/API-based LLM inference
* JSON
* Pandas

---

## 🚀 Instalasi

Clone repository:

```bash
git clone https://github.com/ardifjar443/text-to-sql.git
cd text-to-sql
```

Buat virtual environment:

```bash
python -m venv venv
```

Aktifkan environment pada Windows:

```bash
venv\Scripts\activate
```

Install dependency:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Konfigurasi

Sesuaikan konfigurasi database dan model pada file konfigurasi project.

Contoh:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=dtsen
```

API key dan konfigurasi model sebaiknya disimpan menggunakan environment variable dan **tidak di-commit ke repository**.

Tambahkan file berikut ke `.gitignore`:

```gitignore
.env
__pycache__/
venv/
*.pyc
```

---

## ▶️ Menjalankan Sistem

Jalankan pipeline pengujian sesuai script yang tersedia pada repository.

Contoh:

```bash
python testing/run_testing.py
```

> Nama script dapat disesuaikan dengan struktur project aktual.

---

## 📁 Output Eksperimen

Hasil eksperimen disimpan dalam format terstruktur, seperti JSON atau CSV, yang berisi informasi:

```text
Question
Generated SQL
Ground Truth SQL
Exact Match
Execution Accuracy
Latency
Prompt Tokens
Completion Tokens
Total Tokens
```

Data tersebut digunakan untuk analisis performa model dan penyusunan hasil penelitian.

---

## 🔐 Privacy

Dataset DTSEN mengandung informasi sosial ekonomi yang bersifat sensitif. Data yang digunakan dalam repository publik harus melalui proses anonimisasi atau masking terhadap informasi yang dapat mengidentifikasi individu.

**Jangan mengunggah data DTSEN asli, credential database, API key, atau informasi pribadi ke repository publik.**

---

## 📚 Research

Project ini dikembangkan sebagai bagian dari penelitian:

> **Evaluasi Pendekatan LLaMA untuk Transformasi Bahasa Alami ke SQL pada Dataset DTSEN**

Fokus penelitian meliputi:

* Text-to-SQL
* LLaMA
* Schema Retrieval
* Embedding
* Semantic Retrieval
* Exact Match
* Execution Accuracy
* Prompt Efficiency
* Generalization

---

## 👨‍💻 Author

**Ardi Fajar Arifin**

Research Project — Text-to-SQL DTSEN

---

## 📄 License

Project ini dikembangkan untuk kebutuhan penelitian dan akademik. Penggunaan dataset dan komponen eksternal mengikuti lisensi serta ketentuan masing-masing sumber.
