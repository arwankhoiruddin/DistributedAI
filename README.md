
# Distributed Data Analysis Platform

Platform ini memisahkan **antarmuka web publik** dengan **runner lokal** (aplikasi Python) yang melakukan pengolahan data.  
Data tetap berada di dekat runner, sedangkan web hanya berfungsi sebagai interface. Komunikasi antara web dan runner dilakukan melalui API publik dengan sistem tugas (task queue).

---

## Arsitektur

- **Web (Public Interface):**
  - Frontend untuk pengguna.
  - Mengirim permintaan analisis atau filter data ke API publik.
  - Menampilkan hasil yang dikirim balik oleh runner.

- **API Server (Coordinator):**
  - Menyimpan informasi runner yang terdaftar.
  - Menerima permintaan proses dari web.
  - Menyampaikan instruksi (task) kepada runner.
  - Menyimpan hasil sementara sebelum dikirim ke web.

- **Runner (Local Python Application):**
  - Berjalan di komputer lokal dengan akses ke data.
  - Mendaftar ke API publik dengan ID unik.
  - Secara periodik mengecek apakah ada task untuknya.
  - Menjalankan task sesuai operation code (misal ambil data, filter, analisis).
  - Mengirim balik hasil ke API.

---

## Alur Proses

1. **Registrasi Runner**
   - Runner mendaftar ke API (`POST /register`) untuk mendapatkan ID/token.
   - Runner mengirim heartbeat secara berkala (`/ping`).

2. **User Request**
   - Pengguna web mengirim permintaan analisis → API server membuat task.

3. **Runner Polling**
   - Runner memanggil endpoint `GET /tasks?runner_id=xxx` untuk mengambil task.
   - API mengembalikan daftar task yang pending.

4. **Runner Eksekusi**
   - Runner menjalankan task sesuai operation code.
   - Hasil dikirim balik dengan `POST /result`.

5. **Web Display**
   - Web membaca hasil task (`GET /result/{task_id}`) dan menampilkannya ke pengguna.

---

## Operation Codes

Task dikontrol dengan kode proses sederhana:

| Code | Deskripsi          |
|------|--------------------|
| 100  | Ambil data mentah  |
| 200  | Filter data        |
| 300  | Analisis model ML  |
| 400  | Export laporan     |

Runner melakukan dispatch berdasarkan kode ini.

---

## Teknologi

- **Runner:** Python (FastAPI, Pandas, scikit-learn, dll.)
- **API Server:** FastAPI / Flask / Node.js (bebas)
- **Frontend:** React / Vue / Laravel
- **Database:** PostgreSQL atau MySQL untuk task management
- **Optional:** Message queue (Redis, RabbitMQ, Kafka) jika butuh skalabilitas tinggi

---

## Keamanan

- Setiap runner menggunakan **token unik**.
- Semua komunikasi harus lewat **HTTPS**.
- Data hasil yang besar disimpan di storage terpisah (misalnya S3/MinIO) dan hanya link yang dikirim ke API.

---

## Roadmap

- [ ] Implementasi API server (registrasi runner, task, result)
- [ ] Implementasi runner dengan polling sederhana
- [ ] Integrasi frontend web
- [ ] Tambah dukungan WebSocket untuk komunikasi real-time
- [ ] Tambah sistem autentikasi pengguna web

---

## Lisensi

MIT License
