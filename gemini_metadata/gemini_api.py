import requests

class GeminiAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.gemini.com/v1"  # Ganti dengan URL yang sesuai
        self.api_key = api_key

    def get_metadata(self, params):
        """Mengambil metadata dari Gemini API."""
        url = f"{self.base_url}/generate_metadata"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")
