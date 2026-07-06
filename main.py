from Testing import tests
from Project import gather_data

def main():
    # run this to test your API key, should print your remaining credits
    #tests.test_prompt_id_generation()

    # run this ONCE to gather the required data
    # gather_data.gather_data()

    tests.test_unique_domains()


if __name__ == "__main__":
    main()