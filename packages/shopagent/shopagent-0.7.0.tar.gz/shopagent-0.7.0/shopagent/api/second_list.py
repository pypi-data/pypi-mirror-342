from .list import get_list_of_items


def get_api_second_list(api_information_url):
    counter = 0
    first_list_found = False
    second_list = []

    while len(second_list) == 0 or not first_list_found:
        second_list = get_list_of_items(api_information_url, counter)
        if len(second_list) > 0 and not first_list_found:
            second_list = []
            first_list_found = True

        counter += 1

    return second_list
