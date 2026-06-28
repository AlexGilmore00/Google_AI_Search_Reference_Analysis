from SerpAPI.api_key_loader import API_KEY

class Prompt:
    def __init__(self, id: str, query: str, location: str) -> None:
        self.id = id
        self.params = {
            "engine": "google",
            "q": query,
            "google_domain": "google.com",
            "hl": "en",
            "gl": "uk",
            "location": location
        }
        