import requests

from SerpAPI.api_key_loader import API_KEY
from SerpAPI.prompt import Prompt
from SerpAPI import prompter


def test_connection() -> int:
    resp = requests.get("https://serpapi.com/account", params={"api_key": API_KEY}).json()
    print(f"searches left: {resp["total_searches_left"]}")
    return resp["total_searches_left"]


def test_prompt() -> None:
    prompt = Prompt("test", "What are some good holidays near me?", 
                    "London Gatwick Airport,England,United Kingdom")
    
    refs = prompter.retrieve_ai_overview_references(prompt, verbose_doc=True)
    print(refs)