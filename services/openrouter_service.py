import requests

from config import Config


class OpenRouterClient:

    def __init__(self):

        self.url = "https://openrouter.ai/api/v1"

        self.headers = {

            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",

            "Content-Type": "application/json"

        }

    def embedding(

        self,

        text,

        model

    ):

        payload = {

            "model": model,

            "input": text

        }

        response = requests.post(

            f"{self.url}/embeddings",

            headers=self.headers,

            json=payload,

            timeout=120

        )

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]