Nah, ini baru makin seru. Jadi dalam repo tunggal, isinya ada **tiga komponen
# Distributed Data Analysis Platform

Repositori ini berisi **tiga komponen utama** untuk sistem analisis data terdistribusi:

1. **WordPress Plugin** – antarmuka berbasis dashboard WordPress.  
2. **API Server** – koordinator komunikasi antara plugin dan runner.  
3. **Runner (Python App)** – aplikasi Python yang melakukan analisis data di mesin lokal.

---

## Struktur Repo

```

/wordpress-plugin/   → Plugin WordPress (dashboard UI)
/api-server/         → API Server (FastAPI/Flask)
/runner/             → Python runner untuk eksekusi analisis

````

---

## Arsitektur

- **WordPress Plugin**
  - User login ke dashboard WordPress.
  - Membuat task analisis dari menu admin.
  - Task dikirim ke API server.

- **API Server**
  - Menyimpan task dari WordPress.
  - Mengatur distribusi task ke runner.
  - Menyediakan endpoint untuk hasil analisis.
  - Autentikasi via API key.

- **Runner**
  - Registrasi ke API server dengan ID/token.
  - Polling task yang tersedia untuknya.
  - Eksekusi task (ambil data, filter, analisis).
  - Kirim hasil kembali ke API server.

---

## Alur Proses

1. **Registrasi Runner**
   - Runner `POST /register` ke API server untuk mendapatkan ID/token.
   - Runner kirim heartbeat (`/ping`) secara berkala.

2. **User Membuat Task**
   - User login ke WordPress dashboard → menu **Data Analysis**.
   - Plugin kirim task ke API server (`POST /task`).

3. **Runner Menangani Task**
   - Runner polling `GET /tasks?runner_id=xxx`.
   - Jalankan task sesuai `operation_code`.
   - Kirim hasil balik ke API server (`POST /result`).

4. **Plugin Menampilkan Hasil**
   - Plugin baca hasil dengan `GET /result/{task_id}`.
   - Dashboard menampilkan hasil ke user.

---

## Operation Codes

| Code | Deskripsi          |
|------|--------------------|
| 100  | Ambil data mentah  |
| 200  | Filter data        |
| 300  | Analisis model ML  |
| 400  | Export laporan     |

---

## Teknologi

- **WordPress Plugin**
  - PHP (WordPress Settings API, Admin Menu, REST API Client)
- **API Server**
  - Python (FastAPI/Flask)
  - Database: PostgreSQL/MySQL (untuk task & hasil)
- **Runner**
  - Python (Requests untuk komunikasi, Pandas/NumPy/scikit-learn untuk analitik)

---

## Cara Menjalankan

### 1. API Server
```bash
cd api-server
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
````

### 2. Runner

```bash
cd runner
pip install -r requirements.txt
python runner.py --server http://localhost:8000 --token <runner_token>
```

### 3. WordPress Plugin

* Copy folder `wordpress-plugin` ke `wp-content/plugins/`
* Aktifkan plugin melalui **WordPress Admin > Plugins**
* Konfigurasi API server URL & API key di **Settings > Data Analysis**

---

## Roadmap

* [ ] API server dasar (register, task, result)
* [ ] Runner polling & eksekusi task sederhana
* [ ] Plugin admin page untuk kirim task
* [ ] Tabel status task di dashboard
* [ ] Visualisasi hasil (tabel/grafik)
* [ ] Notifikasi task selesai
* [ ] Role-based access control di WordPress

---

## Lisensi

MIT License

```