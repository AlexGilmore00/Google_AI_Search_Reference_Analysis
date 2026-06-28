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

    print(f"[prompt log] sending query: {prompt.params['q']}\nfrom: {prompt.params['location']}")
    results = try_client_search(prompt.params)
    if results is None:
        return None

    ai_overview = results.get("ai_overview")
    if not ai_overview:
        print(f"[credit log] no AI overview for this query, 1 credit used\n {c_before - 1} credits left")
        return None
    
    if "page_token" in ai_overview:
        follow_up_results = try_client_search({
            "engine": "google_ai_overview",
            "page_token": ai_overview["page_token"]
        })
        if follow_up_results is None:
            return None
        
        ai_overview = follow_up_results.get("ai_overview", {})

    if verbose_doc:
        # save whole ai overview section as json
        pathlib.Path("SerpAPI/Verbose_Output").mkdir(exist_ok=True)
        filename = f"{prompt.id}__{datetime.datetime.now():%Y%m%d_%H%M%S}.json"
        filepath = pathlib.Path("SerpAPI/Verbose_Output") / filename.replace(" ", "_").replace(":", "-")
        filepath.write_text(json.dumps(ai_overview, indent=2))
    
    c_after = get_remaining_searches()
    print(f"[credit log] {c_before - c_after} credits used this query\n{c_after} credits left")
    return ai_overview.get("references", [])


# tries a client.search with params and catches any errors.
# returns the results if the search was successful
# returns None if an ewrror was caught
def try_client_search(params: dict) -> serpapi.SerpResults | None:
    try:
        results = client.search(params)

    except serpapi.HTTPError as e:
        match e.status_code:
            case 401:
                print(f"[error] invalid API key: {e.error}")
            case 400:
                print(f"[error] bad request — check your params: {e.error}")
            case 429:
                print(f"[error] rate limited or out of searches: {e.error}")
            case _:
                print(f"[error] HTTP {e.status_code}: {e.error}")
        return None
    except serpapi.TimeoutError as e:
        print(f"[error] request timed out: {e}")
        return None
    
    return results