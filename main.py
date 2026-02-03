import json
from datetime import datetime, timedelta

catatan = []
mapel_favorit = []
target_harian = 0  # dalam menit

def muat_dari_file():
    """Memuat data dari file JSON jika ada"""
    global catatan, mapel_favorit, target_harian
    try:
        with open("catatan_belajar.json", "r") as f:
            data = json.load(f)
            catatan = data.get("catatan", [])
            mapel_favorit = data.get("mapel_favorit", [])
            target_harian = data.get("target_harian", 0)
            print("✓ Data berhasil dimuat dari file.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"⚠️  Error membaca file: {e}")

def tambah_catatan():
    print("\n--- Tambah Catatan Belajar ---")
    
    try:
        # Input dari pengguna
        mapel = input("Nama mapel: ").strip()
        if not mapel:
            print("❌ Nama mapel tidak boleh kosong!")
            return
            
        topik = input("Topik yang dipelajari: ").strip()
        if not topik:
            print("❌ Topik tidak boleh kosong!")
            return
            
        durasi_input = input("Durasi belajar (menit): ").strip()
        if not durasi_input.isdigit() or int(durasi_input) <= 0:
            print("❌ Durasi harus berupa angka positif!")
            return
        durasi = int(durasi_input)
        
        # Buat dictionary untuk menyimpan satu catatan
        catatan_baru = {
            "mapel": mapel,
            "topik": topik,
            "durasi": durasi,
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Simpan ke dalam list catatan
        catatan.append(catatan_baru)
        print(f"✓ Catatan '{mapel}' berhasil ditambahkan!")
    except ValueError:
        print("❌ Input tidak valid!")
    except Exception as e:
        print(f"❌ Error: {e}")

def lihat_catatan():
    print("\n--- Daftar Catatan Belajar ---")
    
    # Cek apakah ada catatan
    if len(catatan) == 0:
        print("📭 Belum ada catatan. Mulai tambahkan catatan belajarmu!")
        return
    
    # Tampilkan semua catatan dengan rapi
    for i, c in enumerate(catatan, 1):
        print(f"\n{i}. Mapel: {c['mapel']}")
        print(f"   Topik: {c['topik']}")
        print(f"   Durasi: {c['durasi']} menit")
        if "tanggal" in c:
            print(f"   Tanggal: {c['tanggal']}")

def total_waktu():
    print("\n--- Total Waktu Belajar ---")
    
    # Cek apakah ada catatan
    if len(catatan) == 0:
        print("📭 Belum ada catatan untuk dihitung.")
        return
    
    # Hitung total durasi dari semua catatan
    total = 0
    for c in catatan:
        total += c['durasi']
    
    # Konversi menit ke jam dan menit
    jam = total // 60
    menit = total % 60
    
    # Tampilkan hasil
    print(f"⏱️  Total waktu belajar: {total} menit")
    if jam > 0:
        print(f"   Atau: {jam} jam {menit} menit")

def atur_mapel_favorit():
    print("\n--- Atur Mapel Favorit ---")
    mapel_input = input("Masukkan nama mapel (pisahkan dengan koma): ").strip()
    if not mapel_input:
        print("❌ Input tidak boleh kosong!")
        return
    global mapel_favorit
    mapel_favorit = [m.strip() for m in mapel_input.split(",") if m.strip()]
    print(f"✓ Mapel favorit: {', '.join(mapel_favorit)}")

def filter_per_mapel():
    print("\n--- Filter Catatan per Mapel ---")
    if len(catatan) == 0:
        print("📭 Belum ada catatan.")
        return
    
    mapel_input = input("Cari mapel: ").strip()
    hasil = [c for c in catatan if c['mapel'].lower() == mapel_input.lower()]
    
    if len(hasil) == 0:
        print(f"❌ Tidak ada catatan untuk mapel '{mapel_input}'")
        return
    
    print(f"\n📚 Catatan untuk {mapel_input}:")
    total_durasi = 0
    for i, c in enumerate(hasil, 1):
        print(f"{i}. {c['topik']} ({c['durasi']} menit)")
        total_durasi += c['durasi']
    print(f"\n⏱️  Total: {total_durasi} menit")

def atur_target_harian():
    print("\n--- Atur Target Harian ---")
    global target_harian
    try:
        target_input = input("Target belajar per hari (menit): ").strip()
        if not target_input.isdigit() or int(target_input) <= 0:
            print("❌ Target harus berupa angka positif!")
            return
        target_harian = int(target_input)
        print(f"✓ Target harian: {target_harian} menit")
    except ValueError:
        print("❌ Input tidak valid!")

def simpan_ke_file():
    print("\n--- Simpan ke File ---")
    if len(catatan) == 0:
        print("❌ Tidak ada catatan untuk disimpan.")
        return
    
    try:
        with open("catatan_belajar.json", "w") as f:
            json.dump({
                "catatan": catatan,
                "mapel_favorit": mapel_favorit,
                "target_harian": target_harian,
                "tanggal_simpan": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }, f, indent=2, ensure_ascii=False)
        print("✓ Data berhasil disimpan ke 'catatan_belajar.json'")
    except Exception as e:
        print(f"❌ Error: {e}")

def ringkasan_mingguan():
    print("\n--- Ringkasan Mingguan ---")
    if len(catatan) == 0:
        print("📭 Belum ada catatan.")
        return
    
    # Hitung statistik
    total_durasi = sum(c['durasi'] for c in catatan)
    mapel_unik = set(c['mapel'] for c in catatan)
    mapel_terbanyak = max(mapel_unik, key=lambda x: sum(c['durasi'] for c in catatan if c['mapel'] == x))
    durasi_terbanyak = sum(c['durasi'] for c in catatan if c['mapel'] == mapel_terbanyak)
    
    print(f"\n📊 Statistik Belajar:")
    print(f"   Total catatan: {len(catatan)} entries")
    print(f"   Total durasi: {total_durasi} menit")
    print(f"   Jumlah mapel: {len(mapel_unik)} mapel")
    print(f"   Mapel terfokus: {mapel_terbanyak} ({durasi_terbanyak} menit)")
    
    if target_harian > 0:
        rata_rata = total_durasi // len(catatan) if len(catatan) > 0 else 0
        status = "✓ Mencapai target!" if rata_rata >= target_harian else "⚠️  Perlu ditingkatkan"
        print(f"   Target harian: {target_harian} menit")
        print(f"   Rata-rata per catatan: {rata_rata} menit {status}")

def menu():
    print("\n╔════════════════════════════════╗")
    print("║      📖 STUDY LOG APP 📖      ║")
    print("╚════════════════════════════════╝")
    print("\n📚 Menu Utama:")
    print("   1. Tambah catatan belajar")
    print("   2. Lihat catatan belajar")
    print("   3. Total waktu belajar")
    print("\n⚙️  Pengaturan & Fitur Lanjut:")
    print("   5. Atur mapel favorit")
    print("   6. Filter per mapel")
    print("   7. Atur target harian")
    print("   8. Simpan ke file")
    print("   9. Ringkasan mingguan")
    print("\n   4. Keluar")
    print("─" * 32)


# Muat data saat aplikasi dimulai
if __name__ == "__main__":
    muat_dari_file()
    
    while True:
        menu()
        pilihan = input("Pilih menu (1-9 atau 4 untuk keluar): ").strip()

        if pilihan == "1":
            tambah_catatan()
        elif pilihan == "2":
            lihat_catatan()
        elif pilihan == "3":
            total_waktu()
        elif pilihan == "5":
            atur_mapel_favorit()
        elif pilihan == "6":
            filter_per_mapel()
        elif pilihan == "7":
            atur_target_harian()
        elif pilihan == "8":
            simpan_ke_file()
        elif pilihan == "9":
            ringkasan_mingguan()
        elif pilihan == "4":
            print("\n✓ Terima kasih! Terus semangat belajar! 🚀\n")
            break
        else:
            print("❌ Pilihan tidak valid! Silakan pilih menu yang tersedia.")