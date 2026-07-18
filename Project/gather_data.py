import pandas as pd
import csv
from urllib.parse import urlparse
import pathlib

from SerpAPI.prompt import Prompt
from SerpAPI import prompter
from SerpAPI.locations import LOCATIONS
from Project.prompt_list import PROMPTS

FIELDNAMES = ["prompt_id", "position", "domain", "title", "full_link", "full_query", "full_send_location"]


# loops through every permutation of prompt and location and uses serpAPI to query googles AI mode.
# from there, it retrieves all links cited in the AIs response where applicable and writes it 
# to a specified csv file.
# queries with no AI response of responses with no retrievable links are skipped and not written to the csv
def gather_data(output_path: str = "Project/Data/raw_data.csv", verbose_doc: bool = True) -> None:
    if prompter.get_remaining_searches() < len(PROMPTS) * len(LOCATIONS) * 2:
        print("[data log][WARNING] insufficient remaining searches to gather all requested data")
        return None

    # have csv open throughout data gathering process and write after creating each datapoint 
    # to avoid data loss upon crash
    pathlib.Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    total_rows = 0
    with open(output_path, 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

        for partial_id, query in PROMPTS.items():
            for location in LOCATIONS:
                prompt_id = generate_prompt_id(partial_id, location)
                prompt = Prompt(prompt_id, query, location)
                references = prompter.retrieve_ai_overview_references(prompt, verbose_doc)

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

                    row = {
                        "prompt_id": prompt_id,
                        "position": position,
                        "domain": extract_domain(link),
                        "title": reference.get("title"),
                        "full_link": link,
                        "full_query": query,
                        "full_send_location": location
                    }
                    writer.writerow(row)
                    f.flush()  # forces changes immediately to disc
                    total_rows += 1

                print(f"[data log] created {succ_ref_count} data points. skipped {fail_ref_count} " \
                        "references with irretrievable links")
                
    print(f"[data log][FINISHED] saved {total_rows} rows to '{output_path}'")


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