import regex as reg
import requests as req
import math
import shutil
import os


def Crawl(seed: str) -> str:
    link_filter = {
        'queue':[seed],
        'uniques':set()
    }
    page_content = {

    }

    BASE_URL = seed.rsplit('N', 1)[0]

    while len(link_filter['queue']) > 0: 
        popped = link_filter['queue'].pop(0)

        initial_request = req.get(popped)
        save_data(initial_request.text, "data_parse.txt")
        page_grab = parse_data("data_parse.txt", BASE_URL)

        for absolute in page_grab['filter_list']:
            if absolute not in link_filter['uniques']:
                link_filter['queue'].append(absolute)
                link_filter['uniques'].add(absolute)

                # page_content information
                page_key = absolute.rsplit('/', 1)[1].rstrip('.html')
                page_content[page_key] = dict()
                page_content[page_key]['title'] = page_key

                page_content[page_key]['words'] = list()
                page_content[page_key]['outgoing_links'] = list()

        # make for loop that actually adds stuff to page_count
        for outgoing_link in page_grab['outgoing_links']:
            print(outgoing_link)

            
        
    print(page_content)

    return f'The number of page(s) found: {str(len(link_filter["uniques"]))}'


def save_data(text: str, local_file: str):
    with open(local_file, "w") as data_w:
        data_w.write(text)


def parse_data(local_file: str, BASE_URL: str) -> list:
    page_grab = {
        'filter_list': [],
        'words': [],
        'outgoing_links': []
    }

    with open(local_file, "r") as data_r:
        for line in data_r:
            search_absolute = reg.search('\w-\d+.html', line)
            # search_words = reg.search()
            outgoing_links = 'link'

            if search_absolute:
                page_grab['filter_list'].append(BASE_URL + search_absolute.group(0))
                page_grab['outgoing_links'].append(BASE_URL + search_absolute.group(0))
    return page_grab


print(Crawl('http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html'))