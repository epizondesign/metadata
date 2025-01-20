import os
import csv
from .gemini_api import GeminiAPI

class MetadataGenerator:
    def __init__(self, api_key):
        self.api = GeminiAPI(api_key)

    def add_metadata_to_file(self, file_path, title, description, keywords, output_dir):
        """
        Tambahkan metadata ke file gambar menggunakan EXIF.
        """
        from PIL import Image
        import piexif
        
        # Buka file gambar
        try:
            img = Image.open(file_path)
            exif_dict = piexif.load(img.info.get("exif", b""))
            
            # Tambahkan metadata
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description.encode("utf-8")
            exif_dict["0th"][piexif.ImageIFD.Artist] = title.encode("utf-8")
            exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords.encode("utf-8")
            
            # Simpan gambar dengan metadata baru
            output_path = os.path.join(output_dir, os.path.basename(file_path))
            piexif.insert(piexif.dump(exif_dict), file_path)
            img.save(output_path)
            print(f"Metadata berhasil ditambahkan ke file: {output_path}")
        except Exception as e:
            print(f"Error menambahkan metadata ke file {file_path}: {e}")

    def batch_generate(self, input_file, output_dir):
        """
        Membaca file CSV dan menambahkan metadata ke setiap file gambar.
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Baca file CSV
        with open(input_file, "r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                # Ambil metadata dari setiap baris
                title = row.get("title", "")
                description = row.get("description", "")
                keywords = row.get("keywords", "")
                image_path = row.get("image_path", "")
                
                # Path lengkap file gambar
                full_path = os.path.join("/content/uploaded_files", image_path)
                if not os.path.exists(full_path):
                    print(f"File tidak ditemukan: {full_path}")
                    continue
                
                # Tambahkan metadata ke file
                self.add_metadata_to_file(full_path, title, description, keywords, output_dir)

class VideoMetadataGenerator:
    def __init__(self, api_key):
        self.api = GeminiAPI(api_key)

    def add_metadata_to_video(self, file_path, title, description, keywords, output_dir):
        """
        Tambahkan metadata ke file video (MP4) menggunakan FFmpeg.
        """
        import subprocess
        
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        try:
            # Perintah FFmpeg untuk menambahkan metadata
            cmd = [
                "ffmpeg", "-i", file_path,
                "-metadata", f"title={title}",
                "-metadata", f"description={description}",
                "-metadata", f"keywords={keywords}",
                "-codec", "copy", output_path
            ]
            subprocess.run(cmd, check=True)
            print(f"Metadata berhasil ditambahkan ke video: {output_path}")
        except Exception as e:
            print(f"Error menambahkan metadata ke video {file_path}: {e}")

# File: metadata_generator.py

def batch_generate(self, input_file, media_files, output_dir):
    """
    Memproses file CSV dan menambahkan metadata ke file media.

    Args:
        input_file (str): Path ke file CSV metadata.
        media_files (list): Daftar path file media yang akan diproses.
        output_dir (str): Direktori output untuk file media yang telah diberi metadata.
    """
    import shutil

    # Baca file CSV
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        metadata_list = [row for row in reader]

    # Debug: Periksa jumlah metadata
    print(f"Metadata ditemukan: {len(metadata_list)} entries")

    # Loop file media dan tambahkan metadata
    for idx, media_file in enumerate(media_files):
        if idx < len(metadata_list):  # Pastikan ada metadata untuk file ini
            metadata = metadata_list[idx]
            output_file = os.path.join(output_dir, os.path.basename(media_file))

            # Debug: Info file yang sedang diproses
            print(f"Memproses {media_file} -> {output_file} dengan metadata: {metadata}")

            # Salin file media ke output directory (simulasi penambahan metadata)
            shutil.copy(media_file, output_file)

        else:
            print(f"Warning: Tidak ada metadata untuk file media {media_file}")
