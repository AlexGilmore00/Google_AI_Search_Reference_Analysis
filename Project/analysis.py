import csv
from Project.domain_groups import SEMANTIC_GROUPINGS


def print_domains_and_refcounts(grouped_data_file: str = "Project/Data/grouped_by_prompt.csv") -> None:
    all_group = get_domain_refcount_dict()
    
    all_group_sorted = {key: value for key, value in sorted(all_group.items())}
    print(f"total unique domains: {len(all_group_sorted)}")
    for domain, count in all_group_sorted.items():
        icount = int(count)
        print(f"{domain}: {icount}")


def print_domain_groupings_refcounts(grouped_data_file: str = "Project/Data/grouped_by_prompt.csv") -> None:
    all_group = get_domain_refcount_dict(grouped_data_file)

    for g_name, g_domains in SEMANTIC_GROUPINGS.items():
        g_ref_count = 0
        for domain, count in all_group.items():
            if domain in g_domains:
                g_ref_count += int(count)
        print(f"reference count in domain group {g_name}: {g_ref_count}")


def get_domain_refcount_dict(grouped_data_file: str = "Project/Data/grouped_by_prompt.csv") -> dict[str, str]:
    all_group = {}
    with open(grouped_data_file, 'r', encoding="utf-8") as f:
        data = csv.DictReader(f)
        for row in data:
            if row["group_id"] == "all_prompts":
                all_group = row
                all_group.pop("group_id")
                return all_group       
    # fail case
    print("ERROR: could not find 'all_prompts' row in provided data file. please ensure you are inputting" \
        " a file created by Project.structure_data.group_by_prompt()")
    exit(1)
