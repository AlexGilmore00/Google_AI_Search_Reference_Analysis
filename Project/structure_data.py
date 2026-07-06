import csv


# returns a list of all unique domains in the raw data
def get_unique_domains(filename: str = "Project/Data/raw_data.csv") -> list[str]:
    domains = set()
    with open(filename, encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            domains.add(row["domain"])
    
    return list(domains)

