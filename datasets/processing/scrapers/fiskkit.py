# scraper for https://fiskkit.com/

import requests
import tqdm
import json
from bs4 import BeautifulSoup

from .. import utils
from .. import claimreview

url_list_articles = 'https://api.fiskkit.com/api/v1/articles/'
url_single_article_base = 'https://api.fiskkit.com/api/v1/articles/'
url_single_article_view = 'https://fiskkit.com/articles/'
url_tags_types = ''
my_name = 'fiskkit'
my_location = utils.data_location / my_name


def main():
    fact_checking_urls = []
    tags = requests.get('https://api.fiskkit.com/api/v1/tags').json()
    utils.write_json_with_path(tags, my_location, 'types.json')
    response = requests.get(url_list_articles, params={
        'limit': 10000
    }).json()
    utils.write_json_with_path(response, my_location, 'scraped.json')
    for idx, el in enumerate(tqdm.tqdm(response['articles'])):
        if idx > 10:
            pass
            #break
        #print(el)
        details_url = '{}{}'.format(url_single_article_base, el['id'])
        details = requests.get(details_url).json()
        claim_url = details['article']['scraped_url']
        el_tags = requests.get('{}/doc-review'.format(details_url)).json()
        tag_counts = el_tags['meta']['tag_count_by_triplet']
        label = None
        if tag_counts:
            print(tag_counts)
            truthiness_labels = tag_counts.get('triplet', {})
            if truthiness_labels:
                truthiness_labels = truthiness_labels.get('1', None)
                if truthiness_labels:
                    score = truthiness_labels.get('1', 0) / (truthiness_labels.get('1', 0) + truthiness_labels.get('2', 0) + truthiness_labels.get('3', 0))
                    if score <= 0.30:
                        label = 'fake'
                    elif score >= 0.8:
                        label = 'true'
                    else:
                        label = 'mixed'
        print(label)

        fact_checking_urls.append({
            'url': '{}{}'.format(url_single_article_view, el['id']),
            'source': my_name,
            'title': el['title'],
            'claim_url': claim_url,
            'original_label': json.dumps(tag_counts),
            'label': label
        })

    utils.write_json_with_path(fact_checking_urls, my_location, 'fact_checking_urls.json')