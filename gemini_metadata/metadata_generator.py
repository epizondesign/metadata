import os
import csv
import piexif
from gemini_metadata.gemini_api import GeminiAPI
from PIL import Image

class MetadataGenerator:
    def __init__(self, api_key):
        self.api = GeminiAPI(api_key)

    def batch_generate(self, input_file, output_dir):
        """
        Membaca file input, memproses metadata, dan menyimpannya ke output.
        :param input_file: Path ke file input CSV
        :param output_dir: Direktori untuk menyimpan gambar dengan metadata
        """
        with open(input_file, "r") as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                params = {
                    "title": row["title"],
                    "description": row["description"],
                    "keywords": row["keywords"].split(","),
                }
                try:
                    metadata = self.api.get_metadata(params)
                    self.add_metadata_to_image(row["image_path"], metadata, output_dir)
                except Exception as e:
                    print(f"Error processing row {row}: {e}")

    def add_metadata_to_image(self, image_path, metadata, output_dir):
        """Menambahkan metadata EXIF ke gambar."""
        image = Image.open(image_path)
        exif_dict = piexif.load(image.info["exif"]) if "exif" in image.info else {}

        # Tambahkan metadata yang dihasilkan dari API
        exif_dict["0th"][piexif.ImageIFD.Artist] = metadata.get("artist", "Unknown Artist")
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = metadata.get("description", "")
        
        # Simpan gambar dengan metadata yang sudah ditambahkan
        output_image_path = os.path.join(output_dir, os.path.basename(image_path))
        image.save(output_image_path, "JPEG", exif=piexif.dump(exif_dict))
        print(f"Metadata added to: {output_image_path}")

import ffmpeg

class VideoMetadataGenerator(MetadataGenerator):
    def add_metadata_to_video(self, video_path, metadata, output_dir):
        """Menambahkan metadata ke file video."""
        output_video_path = os.path.join(output_dir, os.path.basename(video_path))
        
        # Menambahkan metadata ke video
        ffmpeg.input(video_path).output(output_video_path, 
                                        metadata_title=metadata.get("title", ""), 
                                        metadata_artist=metadata.get("artist", "Unknown Artist"), 
                                        metadata_description=metadata.get("description", "")).run()
        print(f"Metadata added to video: {output_video_path}")
