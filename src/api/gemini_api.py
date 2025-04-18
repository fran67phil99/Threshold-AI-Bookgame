import os
from dotenv import load_dotenv
import requests

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class GeminiAPI:
    def __init__(self, api_key=GEMINI_API_KEY):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    def send_request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError("Unsupported HTTP method")

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        return response.json()

    def get_agent_response(self, prompt):
        url = self.base_url + f"?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        # Adatta questa parte in base alla risposta effettiva di Gemini
        return {"response": response.json()["candidates"][0]["content"]["parts"][0]["text"]}
