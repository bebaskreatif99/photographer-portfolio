import os
from flask import Flask, render_template

# Konfigurasi ini PENTING dan sudah benar
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# --- DATA PAKET HARGA (Tidak berubah) ---
event_packages = [
    { "name": "Bronze", "price": "Rp 800.000", "features": ["1 Photographer", "All digital files", "20 Edited Photos", "Durasi 4 Jam"], "highlight": False },
    { "name": "Silver", "price": "Rp 1.500.000", "features": ["1 Photographer", "All digital files", "30 Edited Photos", "1 menit Video Reels", "Untuk 1 hari event"], "highlight": True },
    { "name": "Gold", "price": "Rp 3.000.000", "features": ["1 Photographer & 1 Videographer", "2-3 menit Video Cinematic", "All Digital Files", "50 Edited Photos", "1 Magazine Book", "Untuk 2 hari event"], "highlight": False }
]
prewedding_packages = [
    { "name": "Bronze", "price": "Rp 1.000.000 - 1.200.000", "features": ["1 Photographer", "All digital files", "20 Edited Photos", "1 Cetak 12Rs + Frame", "Durasi 4 Jam", "Studio / Outdoor"], "highlight": False },
    { "name": "Silver", "price": "Rp 2.000.000", "features": ["1 Photographer", "All digital files", "30 Edited Photos", "1 Cetak 16Rs + Frame", "Max. 8 Jam", "Studio + Outdoor"], "highlight": True },
    { "name": "Gold", "price": "Rp 4.000.000", "features": ["1 Photographer & 1 Videographer", "2-3 menit Video Cinematic", "All Digital Files", "50 Edited Photos", "1 Magazine Book", "2 Cetak 16Rs + Frame", "Max. 10 Jam", "Termasuk Make up + Kostum"], "highlight": False }
]
wedding_packages = [
    { "name": "Bronze", "price": "Rp 1.500.000", "features": ["1 Photographer", "All digital files", "20 Edited Photos", "1 Magazine Book", "Durasi 4 Jam"], "highlight": False },
    { "name": "Silver", "price": "Rp 2.500.000", "features": ["2 Photographer", "All digital files", "30 Edited Photos", "1 Magazine Book", "Max. 8 Jam"], "highlight": True },
    { "name": "Gold", "price": "Rp 5.500.000", "features": ["2 Photographer & 1 Videographer", "2-3 menit Video Cinematic", "All Digital Files", "50 Edited Photos", "1 Magazine Book (100 foto)", "2 Cetak 16Rs + Frame", "Max. 10 Jam"], "highlight": False }
]

# --- FUNGSI OTOMATIS PEMBACA GAMBAR ---
def load_portfolio_images():
    """Membaca file gambar dari subfolder di dalam static/images."""
    portfolio = {'wedding': [], 'prewedding': [], 'event': []}
    base_path = os.path.join(app.static_folder, 'images')
    categories = ['wedding', 'prewedding', 'event']
    
    for category in categories:
        category_path = os.path.join(base_path, category)
        try:
            if os.path.isdir(category_path):
                # Filter hanya file dengan ekstensi gambar yang umum
                image_files = [f for f in os.listdir(category_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
                for filename in image_files:
                    portfolio[category].append({
                        # Path ini akan digunakan di dalam template HTML
                        'src': f'images/{category}/{filename}',
                        # Alt text otomatis untuk aksesibilitas
                        'alt': f'{category.capitalize()} portfolio image: {filename}'
                    })
        except FileNotFoundError:
            # Jika folder tidak ditemukan, lewati saja.
            print(f"Warning: Directory not found at {category_path}")
            pass
            
    return portfolio

# --- ROUTES HALAMAN ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/portfolio')
def portfolio():
    # Panggil fungsi untuk mendapatkan daftar gambar secara dinamis
    images = load_portfolio_images()
    return render_template('portfolio.html', images=images)

@app.route('/pricelist')
def pricelist():
    return render_template(
        'pricelist.html',
        event_data=event_packages,
        prewedding_data=prewedding_packages,
        wedding_data=wedding_packages
    )

if __name__ == "__main__":
    app.run(debug=True)