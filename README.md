# gemini_metadata
# Gemini Metadata Batch Generator

## Deskripsi
Tools untuk menghasilkan metadata secara batch menggunakan API Gemini, ditujukan untuk gambar dan video microstock. Metadata akan langsung dimasukkan ke dalam file gambar (EXIF) atau video.

## Fitur
- Menghasilkan metadata untuk gambar dan video menggunakan API Gemini.
- Metadata disisipkan langsung ke dalam file gambar (EXIF) atau video (menggunakan metadata seperti title, artist, description).
- Mendukung pemrosesan batch dengan file CSV input.

## Cara Penggunaan

### 1. Persiapan
Pastikan Anda sudah memiliki API Key dari Gemini. Anda dapat mendaftarkan API Key di [Gemini API](https://gemini.com).

### 2. Install Dependencies
1. Clone repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Install dependencies:
pip install -r requirements.txt
3. Struktur File Input
File input harus berbentuk CSV dengan header:
title,description,keywords,image_path
title: Judul gambar atau video.
description: Deskripsi gambar atau video.
keywords: Kata kunci yang dipisahkan oleh koma.
image_path: Path ke file gambar (untuk gambar) atau path ke file video (untuk video).
4. Menjalankan Proses
Untuk Gambar (EXIF Metadata)
from gemini_metadata.metadata_generator import MetadataGenerator

# Ganti dengan API Key Anda
api_key = "YOUR_API_KEY"
generator = MetadataGenerator(api_key)

# Jalankan batch processing untuk gambar
generator.batch_generate("input.csv", "output_dir")
Untuk Video (Metadata Video)
from gemini_metadata.metadata_generator import VideoMetadataGenerator

# Ganti dengan API Key Anda
api_key = "YOUR_API_KEY"
video_generator = VideoMetadataGenerator(api_key)

# Jalankan batch processing untuk video
video_generator.batch_generate("input.csv", "output_dir")
