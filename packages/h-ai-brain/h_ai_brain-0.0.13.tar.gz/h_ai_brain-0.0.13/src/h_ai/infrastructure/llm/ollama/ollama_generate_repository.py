import uuid

import requests

from ....domain.reasoning.llm_generate_respository import LlmGenerateRepository


class OllamaGenerateRepository(LlmGenerateRepository):

    def __init__(self, api_url: str, model_name: str, system_prompt: str = None, temperature: float = None, seed: int = None):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.api_url = api_url
        self.temperature = temperature
        self.seed = seed


    def generate(self, user_prompt: str, system_prompt: str = None, session_id: str = None) -> str|None:
        url = f"{self.api_url}/generate"
        random_guid = uuid.uuid4()
        guid_str = str(random_guid)
        system_prompt = system_prompt or self.system_prompt
        payload = {
            "model": self.model_name,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "session": guid_str,
            "num_ctx": "5000",
            "temperature": "0.6"
        }

        if session_id:
            payload["session"] = session_id
        if self.seed:
            payload["seed"] = self.seed
        if self.temperature:
            payload["temperature"] = self.temperature

        try:
            print(payload)
            response = requests.post(url, json=payload)
            response.raise_for_status()

            print(response.json())

            response_content = response.json()["response"]
            return clean_llm_response(response_content)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API call: {e}")
            return None

