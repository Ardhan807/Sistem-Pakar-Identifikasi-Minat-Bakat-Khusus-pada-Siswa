# Sistem-Pakar-Identifikasi-Minat-Bakat-Khusus-pada-Siswa
## 📘 Deskripsi Proyek
Proyek ini merupakan implementasi ulang berbasis Python dan Flask dari sistem pakar yang dijelaskan pada jurnal berjudul

"Sistem Pakar Menggunakan Metode Certainty Factor dalam Identifikasi Pengembangan Minat dan Bakat Khusus pada Siswa" 

Sistem ini dirancang untuk mengidentifikasi pengembangan minat dan bakat khusus pada siswa menggunakan metode Certainty Factor (CF). Melalui antarmuka web sederhana berbasis HTML dan CSS, pengguna (siswa) dapat menjawab sejumlah pertanyaan, dan sistem akan menghitung tingkat kepastian (CF) terhadap kategori minat dan bakat tertentu.

## 🚀 Cara Menjalankan Proyek
- buka terminal
- arahkan ke folder -> contoh masukkan ke dalam terminal "cd C:\Users\Downloads\Sistem_Pakar"
- install flask -> masukkan ke dalam terminal "pip install flask"
- jalankan user interface -> masukkan ke dalam terminal "python user_interface.py"
- buka browser dan kunjungi atau langsung ctrl + click pada terminal -> http://127.0.0.1:5000
- untuk kembali ke cd C:\Users\angga\Downloads\Sistem_Pakar tekan ctrl + c

## ⚙️ Teknologi yang Digunakan
Python 3.11 - menarik kesimpulan (inference) berdasarkan pengetahuan (rules/fakta) yang tersimpan di Knowledge Base dan antarmuka pengguna berbasis Flask
Flask — web framework untuk menjalankan server dan routing.
JSON — menyimpan basis pengetahuan (knowledge base) berupa kondisi, aturan, dan nilai CF.
HTML & CSS — membangun antarmuka pengguna.

## 🧩 Struktur Proyek
📦 sistem-pakar
├── inference_engine.py      # Mesin inferensi (logika Certainty Factor)
├── knowleadge_base.json     # Basis pengetahuan (ciri, aturan, kesimpulan)
├── user_interface.py        # Aplikasi Flask (antarmuka web), desain tampilan menggunakan Html dan css
└── README.md                # Cara menjalankan proyek

## 📚 Referensi
[Artikel: Sistem Pakar Menggunakan Metode Certainty Factor dalam
Identifikasi Pengembangan Minat dan Bakat Khusus pada Siswa](https://www.jsisfotek.org/index.php/JSisfotek/article/view/43)

