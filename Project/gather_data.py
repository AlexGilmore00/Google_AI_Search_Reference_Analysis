import pandas as pd
from urllib.parse import urlparse
import pathlib

from SerpAPI.prompt import Prompt
from SerpAPI import prompter
from SerpAPI.locations import LOCATIONS
from Project.prompt_list import PROMPTS


def gather_data(output_path: str = "Project/Data/raw_data.csv") -> None:
    if prompter.get_remaining_searches() < len(PROMPTS) * len(LOCATIONS) * 2:
        print("[data log][WARNING] insufficient remaining searches to gather all requested data")
        return None

    rows = []

    for partial_id, query in PROMPTS.items():
        for location in LOCATIONS:
            prompt_id = generate_prompt_id(partial_id, location)
            prompt = Prompt(prompt_id, query, location)
            references = prompter.retrieve_ai_overview_references(prompt)

            if not references:
                print(f"[prompt log][FAILURE] failed to find references for prompt '{prompt_id}', " \
                    "this prompt has been passed over")
                continue

            print("[prompt log][SUCCESS] found references, creating datapoints...")

            succ_ref_count = 0
            fail_ref_count = 0
            for position, reference in enumerate(references, start=1):
                link = reference.get("link", "")
                if not link:
                    fail_ref_count += 1
                    continue
                succ_ref_count += 1

                rows.append({
                    "prompt_id": prompt_id,
                    "position": position,
                    "domain": extract_domain(link),
                    "title": reference.get("title"),
                    "full_link": link,
                    "full_query": query,
                    "full_send_location": location
                })
            print(f"[data log] created {succ_ref_count} data points. skipped {fail_ref_count} " \
                    "references with irretrievable links")
            
    df = pd.DataFrame(rows)

    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[data log][FINISHED] saved {len(df)} rows to '{output_path}'")


# extracts the domain given a link. also removes 'www.' if present
# if link is invalid, return empty string
def extract_domain(link: str) -> str:
    if not link:
        return ""
    domain = urlparse(link).netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


def generate_prompt_id(partial_id: str, location: str) -> str:
    loc_parts = location.split(',')
    # append the most precise part of the location (usually city name) to the end of the partial id
    return f"{partial_id}_from:{loc_parts[0]}"