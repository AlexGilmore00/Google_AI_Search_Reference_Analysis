import pandas

from SerpAPI.locations import LOCATIONS
from Project.prompt_list import PROMPTS

def gather_data() -> None:
    for partial_id, prompt in PROMPTS.items():
        for location in LOCATIONS:
            pass


def generate_prompt_id(partial_id: str, location: str) -> str:
    loc_parts = location.split(',')
    # append the most precise part of the location (usually city name) to the end of the partial id
    return f"{partial_id}_from:{loc_parts[0]}"