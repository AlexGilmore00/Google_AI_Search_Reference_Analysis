from Testing import tests
from Project import gather_data, structure_data, analysis

def main():
    # run this to test your API key, should print your remaining credits
    tests.test_connection()

    # run this ONCE to gather the required data
    # gather_data.gather_data()

    # run this after running gather_data() to create a new csv grouping prompts by type
    # accompanied by a tally count for every domain referenced within that group
    # structure_data.group_by_prompt()

    # run this after running structure_data(). This will output the ref counts for all domains
    # references across all prompts sorted in alphabetical order by domian
    # analysis.print_domains_and_refcounts()


if __name__ == "__main__":
    main()