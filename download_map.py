import urllib.request
import os
import json

# 1. Buat folder geo jika belum ada
os.makedirs('geo', exist_ok=True)

# 2. URL GeoJSON Provinsi Indonesia yang paling stabil & ringan
url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/refs/heads/master/indonesia.geojson"
file_path = "geo/indonesia.geojson"

print("⏳ Sedang mengunduh peta Indonesia...")
urllib.request.urlretrieve(url, file_path)
print("✅ Peta berhasil disimpan di: geo/indonesia.geojson!")

# 3. Mengintip isi format datanya agar kita tahu cara menyambungkannya
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    contoh_provinsi = data['features'][0]['properties']
    print("\n🔍 CONTOH ISI DATA PROVINSI DI DALAM PETA:")
    print(contoh_provinsi)