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

    for domain, count in all_group.items():
        icount = int(count)
        print(f"{domain}: {icount}")
