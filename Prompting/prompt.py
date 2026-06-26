from Prompting.api_key_loader import API_KEY

class Prompt:
    def __init__(self, query: str, location: str) -> None:
        self.params = {
            "api_key": API_KEY,
            "engine": "google_ai_engine",
            "q": query,
            "google_domain": "google.com",
            "hl": "en",
            "gl": "uk",
            "location": location
        }
        