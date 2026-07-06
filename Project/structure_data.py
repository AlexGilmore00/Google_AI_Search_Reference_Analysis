import csv


# returns a list of all unique domains in the raw data
def get_unique_domains(filename: str = "Project/Data/raw_data.csv") -> list[str]:
    domains = set()
    with open(filename, encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            domains.add(row["domain"])
    
    return list(domains)


# takes the input of the path for a raw data file created by gather_data.gather_data()
# creates a new csv with rows that group the all the prompts into categories based on the style
# of prompt (e.g. where the prompt was sent from or what ares its targeting). 
# prompts can be in multiple categories at the same time.
# from their, tally up how many times each domain apears in prompts fitting into a specific group
# e.g. final csv in format:
# group_id, instagram.com, reddit.com, tripadvisor.com, ...
# what_style_prompts, 4, 8, 0, ...
def group_by_prompt(in_file: str = "Project/Data/raw_data.csv", 
                    out_file: str = "Project/Data/grouped_by_prompt.csv") -> None:
    # get unique domains here as we'll alreadt be reading the whole raw file
    domains = set()

    # init data groups
    what_group = {"group_id": "what_style_prompts"}
    how_group = {"group_id": "how_style_prompts"}
    context_group = {"group_id": "with_context_prompts"}
    no_context_group = {"group_id": "without_context_prompts"}
    about_scot = {"group_id": "about_scotland"}
    about_eng = {"group_id": "about_england"}
    about_local = {"group_id": "about_local"}
    from_location = {
        "London": {"group_id": "from_london"},
        "Bristol": {"group_id": "from_bristol"},
        "Cleethorpes": {"group_id": "from_cleethropes"},
        "Manchester": {"group_id": "from_manchester"},
        "York": {"group_id": "from_york"},
        "Newcastle upon Tyne": {"group_id": "from_newcastle"},
        "Edinburgh": {"group_id": "from_edinburgh"},
        "Inverness": {"group_id": "from_inverness"},
        "Glasgow": {"group_id": "from_glasgow"}
    }  # each key lines up perfectly with the 'from location' part of the prompt ids

    # group data
    with open(in_file, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # get unique domains whiel already reading
            domain = row["domain"]
            domains.add(domain)

            # decode prompt id
            id_parts = row["prompt_id"].split("_")
            style_indicator = id_parts[0]
            context_indicator = id_parts[1]
            about_loc_indicator = id_parts[2]
            from_loc_indicator = id_parts[3].split(":")[1]

            # add domain to corresponding group
            # prompt style
            if style_indicator == "what":
                if domain not in what_group:
                    what_group[domain] = "1"
                else:
                    what_group[domain] = str(int(what_group[domain]) + 1)
            elif style_indicator == "how":
                if domain not in how_group:
                    how_group[domain] = "1"
                else:
                    how_group[domain] = str(int(how_group[domain]) + 1)

            # context
            if context_indicator == "con":
                if domain not in context_group:
                    context_group[domain] = "1"
                else:
                    context_group[domain] = str(int(context_group[domain]) + 1)
            elif context_indicator == "ncon":
                if domain not in no_context_group:
                    no_context_group[domain] = "1"
                else:
                    no_context_group[domain] = str(int(no_context_group[domain]) + 1)

            # targeted location
            if about_loc_indicator == "local":
                if domain not in about_local:
                    about_local[domain] = "1"
                else:
                    about_local[domain] = str(int(about_local[domain]) + 1)
            elif about_loc_indicator == "eng":
                if domain not in about_eng:
                    about_eng[domain] = "1"
                else:
                    about_eng[domain] = str(int(about_eng[domain]) + 1)
            elif about_loc_indicator == "scot":
                if domain not in about_scot:
                    about_scot[domain] = "1"
                else:
                    about_scot[domain] = str(int(about_scot[domain]) + 1)

            # from location
            if domain not in from_location[from_loc_indicator]:
                from_location[from_loc_indicator][domain] = "1"
            else:
                from_location[from_loc_indicator][domain] = str(int(from_location[from_loc_indicator][domain]) + 1)
    
    # fill in any missing domains with value 0
    write_rows = [what_group, how_group, context_group, no_context_group, about_scot, about_eng, about_local,
                  from_location["Bristol"], from_location["Cleethorpes"], from_location["Edinburgh"],
                  from_location["Glasgow"], from_location["Inverness"], from_location["London"], 
                  from_location["Manchester"], from_location["Newcastle upon Tyne"], from_location["York"]]

    for row in write_rows:
        for domain in domains:
            if domain not in row:
                row[domain] = "0"
    
    print(write_rows)
    
    # write the new csv file
    header = ["group_id"]
    for domain in domains:
        header.append(domain)

    with open(out_file, 'w', encoding="utf-8", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(write_rows)

    



