import sys
import re
from os import mkdir
from concurrent.futures import ThreadPoolExecutor

import requests

IN_FILE = 'samples_urls'
OUT_DIR = 'samples_pages'

def get_urls() -> [str]:
    with open(IN_FILE, 'r') as file:
        # get each url and drop \n at the end
        return [url[:-1] for url in file.readlines()]

def fetch_page(url) -> str:
    req = requests.get(url)
    return req.content.decode(encoding='utf-8')

def save_page(content: str, number: int, domain: str):
    with open('{}/page-{}-[{}]'.format(OUT_DIR, number, domain), 'w') as file:
        file.write(content)

def fetch_save_page(url: str, number: int):
    domain = re.search(r"\.(\w*)\.", url)
    content = fetch_page(url)
    save_page(content, number, domain.group(1))

def download(concurrency: int):
    try:
        mkdir(OUT_DIR)
    except FileExistsError:
        pass
    
    urls = get_urls()
    with ThreadPoolExecutor(max_workers=concurrency-1) as executor:
        index = 1
        for url in urls:
            executor.submit(fetch_save_page, url, index)
            index += 1

if __name__ == '__main__':
    num_args = len(sys.argv) - 1
    if num_args != 1:
        print('Wrong number of command-line arguments. Expected 1 (concurrency number), received {}'.format(num_args), file=sys.stderr)
        sys.exit(1)

    concurrency = int(sys.argv[1])
    download(concurrency)