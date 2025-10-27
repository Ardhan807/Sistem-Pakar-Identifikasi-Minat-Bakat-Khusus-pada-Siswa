from flask import Flask, request, render_template_string, redirect, url_for
from inference_engine import load_knowledge_base, infer
import os

app = Flask(__name__)

# Muat knowledge base
KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")
kb = load_knowledge_base(KB_PATH)

# Buat dua halaman
INDEX_HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Identifikasi Minat & Bakat Siswa</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body{ font-family: Arial, sans-serif; max-width:900px; margin:20px auto; padding:10px; }
    .q { margin:12px 0; padding:8px; border-bottom:1px solid #eee; }
    label { margin-right:12px; }
    .btn { padding:10px 18px; background:#1976d2; color:white; border:none; cursor:pointer; border-radius:6px; }
    .btn:hover { background:#125ea8; }
    header h1 { margin:0 0 10px 0; }
    .note { color:#444; font-size:0.9rem; margin-bottom:8px; }
  </style>
</head>
<body>
  <header>
    <h1>Identifikasi Pengembangan Minat & Bakat Khusus</h1>
    <p class="note">Jawab setiap pertanyaan dengan Ya/Tidak, lalu klik <strong>Submit</strong>.</p>
  </header>

  <form method="post" action="{{ url_for('evaluate') }}">
    {% for cid, text in conditions %}
      <div class="q">
        <div><strong>{{ loop.index }}. {{ text }}</strong></div>
        <label><input type="radio" name="{{ cid }}" value="ya" required> Ya</label>
        <label><input type="radio" name="{{ cid }}" value="tidak" required checked> Tidak</label>
      </div>
    {% endfor %}

    <div style="margin-top:16px;">
      <button class="btn" type="submit">Submit</button>
    </div>
  </form>
</body>
</html>
"""

RESULT_HTML = """
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Hasil Identifikasi</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    td:nth-child(2) { text-align: center; }  /* Nilai CF di tengah */
    h1, h3 { color:#1976d2; text-align:center; }
    body{ font-family: Arial, sans-serif; max-width:800px; margin:20px auto; padding:10px; }
    .card{ padding:14px; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06); background:#fff; }
    .bakat { margin:8px 0; padding:8px; border-bottom:1px dashed #eee; }
    .top { background:#f5faff; padding:10px; border-radius:6px; margin-bottom:12px; }
    a.btn { display:inline-block; padding:8px 14px; background:#1976d2; color:white; text-decoration:none; border-radius:6px; }
  </style>
</head>
<body>
  <h1>Hasil Identifikasi</h1>

  <div class="card">
    {% if results %}
      <div class="top">
        <strong>Bakat Dominan: </strong>
        {{ results[0]['bakat'] }} (CF = {{ results[0]['cf'] }})
      </div>

      <h3>Detail Semua Bakat (urut CF)</h3>
      {% for r in results %}
        <div class="bakat">
          <strong>{{ loop.index }}. {{ r['bakat'] }}</strong><br>
          CF: {{ r['cf'] }}
        </div>
      {% endfor %}
    {% else %}
      <p>Tidak ada aturan yang terpenuhi berdasarkan jawaban Anda.</p>
    {% endif %}
  </div>
  <h3>Tabel Skala Keyakinan</h3>
  <table>
    <tr><th>Tingkat Keyakinan</th><th>Nilai CF</th></tr>
    <tr><td>Pasti Tidak</td><td>0.0</td></tr>
    <tr><td>Hampir Pasti Tidak</td><td>0.1</td></tr>
    <tr><td>Kemungkinan Besar Tidak</td><td>0.2</td></tr>
    <tr><td>Mungkin Tidak</td><td>0.3</td></tr>
    <tr><td>Tidak Tahu</td><td>0.4</td></tr>
    <tr><td>Mungkin</td><td>0.5</td></tr>
    <tr><td>Kemungkinan Besar</td><td>0.6</td></tr>
    <tr><td>Hampir Pasti</td><td>0.8</td></tr>
    <tr><td>Pasti</td><td>1.0</td></tr>
  </table>

  <div style="margin-top:14px;">
    <a class="btn" href="{{ url_for('index') }}">Kembali</a>
  </div>
</body>
</html>
"""

# Route utama (halaman awal) aplikasi
@app.route("/", methods=["GET"])
def index():
    # Mengambil daftar kondisi dari knowledge base (pertanyaan-pertanyaan)
    # Formatnya dijadikan list of tuple: [(id_kondisi, teks_pertanyaan), ...]
    conditions = [(cid, data["text"]) for cid, data in kb["conditions"].items()]

    # Mengurutkan daftar kondisi berdasarkan ID (C01, C02, dst)
    conditions.sort()

    # Menampilkan halaman HTML utama (template) dengan daftar pertanyaan
    # INDEX_HTML adalah template HTML yang berisi form untuk menjawab pertanyaan
    return render_template_string(INDEX_HTML, conditions=conditions)

# Route untuk memproses hasil jawaban pengguna
@app.route("/evaluate", methods=["POST"])
def evaluate():
    # Dictionary untuk menyimpan jawaban pengguna
    answers = {}

    # Loop setiap kondisi yang ada di knowledge base
    for cid in kb["conditions"].keys():
        # Ambil nilai dari form HTML (input pengguna)
        # Jika tidak diisi, default "tidak"
        v = request.form.get(cid, "tidak").lower()

        # Ubah nilai menjadi boolean: True jika 'ya', False jika 'tidak'
        answers[cid] = (v == "ya")

    # Panggil fungsi infer() untuk melakukan penalaran berbasis rule dan CF
    # Hasilnya berupa daftar bakat dengan nilai CF
    results = infer(answers, kb)

    # Tampilkan halaman hasil (template HTML hasil evaluasi)
    # RESULT_HTML adalah template yang menampilkan daftar bakat dan nilai CF-nya
    return render_template_string(RESULT_HTML, results=results)

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    # Jalankan server Flask dalam mode debug
    # Mode debug memudahkan pengembang karena auto-reload dan tampil error detail
    app.run(debug=True)
