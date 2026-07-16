import requests

from SerpAPI.api_key_loader import API_KEY
from SerpAPI.prompt import Prompt
from SerpAPI import prompter
from SerpAPI import locations
from Project.gather_data import generate_prompt_id
from Project.prompt_list import PROMPTS
from Project.structure_data import get_unique_domains


def test_connection() -> int:
    resp = requests.get("https://serpapi.com/account", params={"api_key": API_KEY}).json()
    print(f"searches left: {resp["total_searches_left"]}")
    return resp["total_searches_left"]


def test_prompt() -> None:
    prompt = Prompt("test", "What are some good holidays near me?", locations.LONDON)
    refs = prompter.retrieve_ai_overview_references(prompt, verbose_doc=True)
    print(refs)


def test_prompt_id_generation() -> None:
    partial_id = list(PROMPTS.keys())[0]
    for location in locations.LOCATIONS:
        full_id = generate_prompt_id(partial_id, location)
        print(f"{partial_id} -> {full_id}")


def test_unique_domains() -> None:
    doms = get_unique_domains()
    print(doms)