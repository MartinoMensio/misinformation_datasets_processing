#!/usr/bin/env python

import re

from .. import utils
from .. import claimreview

subfolder = utils.data_location / 'pontes_fakenewssample'

def clean_url(url):
    url = re.sub(r'&(amp;)+', '&', url)
    return url

def main():
    data = utils.read_tsv(subfolder / 'source' / 'resized_v2.csv', delimiter=',')

    print(len(data))
    print('loaded data')
    types = set([el['type'] for el in data])
    print(types)
    urls = [{'url': clean_url(el['url']), 'label': claimreview.simplify_label(el['type']), 'source': 'pontes_fakenewssample'} for el in data if el['type']]
    urls = [el for el in urls if el['label']]

    utils.write_json_with_path(urls, subfolder, 'urls.json')
    del data

    by_domain = utils.compute_by_domain(urls)

    utils.write_json_with_path(by_domain, subfolder, 'domains.json')
