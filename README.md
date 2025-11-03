# Prediksi Biaya Tagih Fasilitas Kesehatan (Penyakit Tuberkulosis)
## 📘 Deskripsi Proyek
Proyek ini menggunakan **Random Forest Regression** untuk memprediksi **biaya tagih oleh fasilitas kesehatan (provider)** pada pasien dengan penyakit **Tuberkulosis**, berdasarkan data **BPJS Kesehatan Tahun 2022**.  

Model ini membantu fasilitas kesehatan dalam:
- Analisis biaya layanan pasien Tuberkulosis  
- Perencanaan anggaran  
- Memahami pola klaim biaya pasien  

## 🚀 Cara Menjalankan Proyek
buka terminal
- arahkan ke folder contoh masukkan ke dalam terminal
  ```
  cd C:\Users\Downloads\Sistem-Pakar-Identifikasi-Minat-Bakat-Khusus-pada-Siswa
  ```
- install flask masukkan ke dalam terminal
  ```
  pip install flask
  ```
- jalankan user interface masukkan ke dalam terminal
  ```
  python user_interface.py
  ```
- buka browser
  kunjungi atau langsung ctrl + click pada terminal
  ```
  http://127.0.0.1:5000
  ```

## ⚙️ Teknologi yang Digunakan
- Python 3.11 → preprocessing data, training model, dan prediksi
- Scikit-Learn → implementasi Random Forest Regression dan evaluasi model
- Pandas & NumPy → manipulasi dan analisis data
- Matplotlib / Seaborn → visualisasi data dan hasil prediksi

## 🧩 Struktur Proyek
```
📦 Prediksi-Biaya-Tagih-TB
├── run_model.py           # Script utama untuk preprocessing, training, dan prediksi
├── data/
│   └── bpjs_tb_2022.csv  # Data klaim pasien Tuberkulosis
├── model/
│   └── random_forest.pkl  # Model Random Forest yang telah dilatih (opsional)
├── requirements.txt       # Library yang dibutuhkan
└── README.md              # Dokumentasi proyek
```

## 📈 Hasil
- Model mampu memprediksi biaya tagih dengan akurasi tinggi menggunakan Random Forest.
- Dapat membantu analisis biaya dan perencanaan anggaran di fasilitas kesehatan.

