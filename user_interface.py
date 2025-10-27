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
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #0056b3;
      --accent: #ffc107;
      --bg-light: #f9fbff;
      --bg-dark: #121212;
      --text-light: #333;
      --text-dark: #eee;
    }

    body {
      font-family: 'Poppins', sans-serif;
      margin: 0;
      padding: 0;
      background: var(--bg-light);
      color: var(--text-light);
      transition: all 0.4s ease;
    }

    header {
      text-align: center;
      padding: 30px 20px;
      background: linear-gradient(135deg, var(--primary), #1976d2);
      color: white;
      border-bottom: 5px solid var(--accent);
    }

    header img {
      width: 80px;
      margin-bottom: 10px;
    }

    main {
      max-width: 900px;
      background: white;
      margin: 30px auto;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .q {
      margin: 18px 0;
      padding: 12px;
      border-left: 5px solid var(--primary);
      background: #f0f6ff;
      border-radius: 10px;
    }

    label {
      margin-right: 15px;
      cursor: pointer;
    }

    .btn {
      display: block;
      margin: 20px auto 0;
      padding: 12px 28px;
      background: var(--primary);
      color: white;
      border: none;
      border-radius: 8px;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.3s;
    }

    .btn:hover {
      background: #003d80;
    }

    footer {
      text-align: center;
      color: #777;
      padding: 20px;
      font-size: 0.9rem;
    }

    /* 🌙 Dark Mode */
    @media (prefers-color-scheme: dark) {
      body { background: var(--bg-dark); color: var(--text-dark); }
      main { background: #1e1e1e; box-shadow: 0 8px 20px rgba(255,255,255,0.05); }
      .q { background: #2a2a2a; border-left-color: var(--accent); }
      .btn { background: var(--accent); color: #111; }
      header { background: linear-gradient(135deg, #0a0a0a, #1a1a1a); border-bottom-color: var(--accent); }
    }
  </style>
</head>
<body>
  <header>
    <img src="https://cdn-icons-png.flaticon.com/512/3135/3135755.png" alt="Ikon Siswa">
    <h1>🧠 Identifikasi Minat & Bakat Siswa</h1>
    <p>Jawab setiap pertanyaan dengan <strong>Ya</strong> atau <strong>Tidak</strong>.</p>
  </header>

  <main>
    <form method="post" action="{{ url_for('evaluate') }}">
      {% for cid, text in conditions %}
        <div class="q">
          <div><strong>{{ loop.index }}. {{ text }}</strong></div>
          <label><input type="radio" name="{{ cid }}" value="ya" required> Ya</label>
          <label><input type="radio" name="{{ cid }}" value="tidak" required checked> Tidak</label>
        </div>
      {% endfor %}
      <button class="btn" type="submit">🚀 Submit Jawaban</button>
    </form>
  </main>

  <footer>
    © 2025 Sistem Identifikasi Minat & Bakat | Dibuat dengan Flask ⚙️
  </footer>
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
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #0056b3;
      --accent: #ffc107;
      --bg-light: #f9fbff;
      --bg-dark: #121212;
      --text-light: #333;
      --text-dark: #eee;
    }

    body {
      font-family: 'Poppins', sans-serif;
      background: var(--bg-light);
      color: var(--text-light);
      margin: 0;
      padding: 0;
      transition: all 0.4s ease;
    }

    header {
      text-align: center;
      background: linear-gradient(135deg, var(--primary), #1976d2);
      padding: 30px 20px;
      color: white;
      border-bottom: 5px solid var(--accent);
    }

    header img {
      width: 80px;
      margin-bottom: 10px;
    }

    main {
      max-width: 800px;
      margin: 30px auto;
      background: white;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .top {
      background: #f5faff;
      padding: 14px;
      border-left: 5px solid var(--primary);
      border-radius: 10px;
      margin-bottom: 16px;
    }

    .bakat {
      margin: 10px 0;
      padding: 10px;
      border-bottom: 1px dashed #ddd;
    }

    h3 { color: var(--primary); margin-top: 20px; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }

    th, td {
      padding: 10px;
      border-bottom: 1px solid #ddd;
    }

    td:nth-child(2) { text-align: center; }

    .btn {
      display: inline-block;
      padding: 10px 16px;
      background: var(--primary);
      color: white;
      border-radius: 8px;
      text-decoration: none;
      margin-top: 20px;
      transition: 0.3s;
    }

    .btn:hover {
      background: #003d80;
    }

    /* 🌙 Dark Mode */
    @media (prefers-color-scheme: dark) {
      body { background: var(--bg-dark); color: var(--text-dark); }
      main { background: #1e1e1e; box-shadow: 0 8px 20px rgba(255,255,255,0.05); }
      .top { background: #2a2a2a; border-left-color: var(--accent); }
      .bakat { border-bottom: 1px dashed #444; }
      table { border-color: #444; }
      th, td { border-bottom: 1px solid #444; }
      .btn { background: var(--accent); color: #111; }
      header { background: linear-gradient(135deg, #0a0a0a, #1a1a1a); border-bottom-color: var(--accent); }
    }
  </style>
</head>
<body>
  <header>
    <img src="https://cdn-icons-png.flaticon.com/512/3135/3135755.png" alt="Ikon Hasil">
    <h1>📊 Hasil Identifikasi Minat & Bakat</h1>
  </header>

  <main>
    {% if results %}
      <div class="top">
        <h2>🏆 Bakat Dominan: {{ results[0]['bakat'] }}</h2>
        <p>Nilai Keyakinan (CF): <strong>{{ results[0]['cf'] }}</strong></p>
      </div>

      <h3>Detail Semua Bakat (Urut Berdasarkan CF)</h3>
      {% for r in results %}
        <div class="bakat">
          <strong>{{ loop.index }}. {{ r['bakat'] }}</strong><br>
          CF: {{ r['cf'] }}
        </div>
      {% endfor %}
    {% else %}
      <p>Tidak ada aturan yang terpenuhi berdasarkan jawaban Anda.</p>
    {% endif %}

    <h3>📈 Tabel Skala Keyakinan</h3>
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

    <a class="btn" href="{{ url_for('index') }}">🔙 Kembali</a>
  </main>
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
