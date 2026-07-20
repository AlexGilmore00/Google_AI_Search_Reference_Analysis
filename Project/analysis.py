import csv


def print_domains_and_refcounts(grouped_data_file: str = "Project/Data/grouped_by_prompt.csv"):
    all_group = {}
    with open(grouped_data_file, 'r', encoding="utf-8") as f:
        data = csv.DictReader(f)
        for row in data:
            if row["group_id"] == "all_prompts":
                all_group = row
                all_group.pop("group_id")
                break
    
    all_group_sorted = {key: value for key, value in sorted(all_group.items())}
    print(f"total unique domains: {len(all_group_sorted)}")
    for domain, count in all_group_sorted.items():
        icount = int(count)
        print(f"{domain}: {icount}")
