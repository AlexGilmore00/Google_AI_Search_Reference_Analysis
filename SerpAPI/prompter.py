import pathlib
import datetime
import json
import requests
import serpapi

from SerpAPI.api_key_loader import API_KEY
from SerpAPI.prompt import Prompt


client = serpapi.Client(api_key=API_KEY)


# returns the number of queries left for the logged in SerpAPI accounf
def get_remaining_searches() -> int:
    resp = requests.get("https://serpapi.com/account", params={"api_key": API_KEY}).json()
    return resp["total_searches_left"]


# returns a dict containing the whole ai overview for a prompt if present
# if not present, returns None
# if couldnt find sources, returns empty list
# verbose_doc saves full ai overview as json to disc
def retrieve_ai_overview_references(prompt: Prompt, verbose_doc: bool = True) -> list[dict] | None:
    c_before = get_remaining_searches()

    print(f"[prompt log] sending query: {prompt.params["q"]}\nfrom: {prompt.params["location"]}")
    results = client.search(prompt.params)

    ai_overview = results.get("ai_overview")
    if not ai_overview:
        print(f"[credit log] no AI overview for this query, 1 credit used\n {c_before - 1} credits left")
        return None
    
    if "page_token" in ai_overview:
        ai_overview = client.search({
            "engine": "google_ai_overview",
            "page_token": ai_overview["page_token"]
        }).get("ai_overview", {})

    if verbose_doc:
        # save whole ai overview section as json
        pathlib.Path("SerpAPI/Verbose_Output").mkdir(exist_ok=True)
        filename = f"{prompt.id}__{datetime.datetime.now():%Y%m%d_%H%M%S}"
        filepath = pathlib.Path("SerpAPIVerbose_Output") / filename.replace(" ", "_")
        filepath.write_text(json.dumps(ai_overview, indent=2))
    
    c_after = get_remaining_searches()
    print(f"[credit log] {c_after - c_before} credits used this query\n{c_after} credits left")
    return ai_overview.get("references", [])