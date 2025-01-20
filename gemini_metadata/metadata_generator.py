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
        from PIL.ExifTags import TAGS
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
            piexif.insert(piexif.dump(exif_dict), file_path, output_path)
            print(f"Metadata berhasil ditambahkan ke file: {output_path}")
        except Exception as e:
            print(f"Error menambahkan metadata ke file {file_path}: {e}")

    def batch_generate(self, input_file, output_dir):
        """
        Membaca file CSV dan menambahkan metadata ke setiap file gambar.
        """
        # Pastikan folder output ada
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
