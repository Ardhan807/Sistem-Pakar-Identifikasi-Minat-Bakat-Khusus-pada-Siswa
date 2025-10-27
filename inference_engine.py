import json
from typing import Dict, List

# Fungsi untuk memuat knowledge base dari file JSON
def load_knowledge_base(file_path: str = "knowledge_base.json") -> dict:
    # Membuka file knowledge base dan memuat isinya sebagai dictionary Python
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# Fungsi untuk menggabungkan dua nilai Certainty Factor (CF)
def combine_cf(cf1: float, cf2: float) -> float:
    """
    Rumus gabungan CF:
    CFcombined = CF1 + CF2 * (1 - CF1)
    Digunakan untuk menggabungkan dua nilai kepastian (misalnya dari dua aturan berbeda)
    """
    return cf1 + cf2 * (1 - cf1)


# Fungsi utama untuk melakukan inferensi (penalaran)
def infer(answers: Dict[str, bool], kb: dict) -> List[dict]:
    """
    Fungsi ini melakukan proses penalaran berbasis aturan (rule-based reasoning)
    dengan pendekatan Forward Chaining dan metode Certainty Factor (CF).
    
    Parameter:
    - answers: dictionary berisi jawaban pengguna (misalnya {"C01": True, "C02": False, ...})
    - kb: knowledge base yang telah dimuat dari file JSON

    Return:
    - List berisi hasil inferensi berupa:
      [{"bakat": "Bakat Musik", "cf": 0.85}, {"bakat": "Bakat Sains", "cf": 0.6}, ...]
      Hasil sudah diurutkan dari CF tertinggi ke terendah.
    """

    # Ambil bagian-bagian dari knowledge base
    conditions = kb["conditions"]  # Daftar kondisi (pertanyaan dan nilai CF jika dijawab "ya")
    rules = kb["rules"]            # Daftar aturan IF-THEN
    bakat_names = kb["bakat"]      # Nama-nama bakat (hasil akhir)

    results = {}  # Dictionary untuk menyimpan hasil akhir (bakat_id -> cf total)

    # Iterasi setiap aturan di knowledge base
    for rule in rules:
        cond_ids = rule["if"]      # Kondisi yang harus terpenuhi untuk aturan ini
        bakat = rule["then"]       # Hasil (bakat) jika kondisi terpenuhi
        rule_cf_weight = rule["cf"]  # Bobot kepastian dari aturan itu sendiri

        # Kumpulan nilai CF dari tiap kondisi
        cf_values = []
        active = True  # Menandakan apakah semua kondisi "aktif" (jawaban "ya")

        # Cek setiap kondisi yang menjadi syarat aturan
        for cid in cond_ids:
            if answers.get(cid, False):
                # Jika dijawab "ya", ambil nilai CF dari kondisi tersebut
                cf_values.append(conditions[cid]["cf_yes"])
            else:
                # Jika salah satu kondisi tidak terpenuhi (jawaban "tidak"), aturan tidak aktif
                active = False
                break

        # Jika aturan tidak aktif, lanjut ke aturan berikutnya
        if not active:
            continue

        # Ambil nilai CF terendah dari semua kondisi (karena logika AND)
        # Lalu dikalikan dengan bobot CF dari aturan
        cf_rule = min(cf_values) * rule_cf_weight

        # Jika bakat ini sudah memiliki nilai CF sebelumnya, gabungkan menggunakan rumus combine_cf
        if bakat in results:
            results[bakat] = combine_cf(results[bakat], cf_rule)
        else:
            # Jika belum ada, simpan langsung
            results[bakat] = cf_rule

    # Urutkan hasil berdasarkan nilai CF tertinggi
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # Format hasil akhir agar lebih mudah dibaca
    final = []
    for b_id, cf_val in sorted_results:
        final.append({
            "bakat_id": b_id,
            "bakat": bakat_names.get(b_id, b_id),  # Ambil nama bakat berdasarkan ID
            "cf": round(cf_val, 4)  # Dibulatkan hingga 4 desimal
        })

    return final